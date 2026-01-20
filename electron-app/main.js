const { app, BrowserWindow, ipcMain, dialog, Notification, Menu } = require("electron");
const { join, basename, dirname } = require("path");
const { readFileSync } = require("fs");
const axios = require("axios");
const { get, post } = axios;
const { spawn } = require("child_process");
//const { fileURLToPath } = require("url");

//const __filename = fileURLToPath(import.meta.url);
//const __dirname = dirname(__filename);

let mainWindow;
let apiProcess;
let botProcess;

const API_PORT = 5000;
const API_URL = `http://localhost:${API_PORT}`;

const menuTemplate = [
    {
        label: 'File',
        submenu: [
            { role: 'quit' }
        ]
    },
    {
        label: 'View',
        submenu: [
            { role: 'reload' },
            { role: 'toggleDevTools' }
        ]
    }
];

const menu = Menu.buildFromTemplate(menuTemplate);
Menu.setApplicationMenu(menu);

function createWindow() {
    mainWindow = new BrowserWindow({
        width: 800,
        height: 600,
        minWidth: 600,
        minHeight: 400,
        webPreferences: {
            preload: join(__dirname, 'preload.js'),
            nodeIntegration: false,
            contextIsolation: true
        },
        //icon: path.join(__dirname, 'assets', 'icon.png'),
        backgroundColor: '#f9fafb',
        show: false
   });

   //show window when ready
   mainWindow.once('ready-to-show', () =>{
         mainWindow.show();
   });

   //load the app 
   mainWindow.loadFile('index.html');

   //open dev tools
   if (process.env.NODE_ENV === 'development') {
       mainWindow.webContents.openDevTools();
   };

   //handle window closed
   mainWindow.on('closed', () => {
         mainWindow = null;
   });

};

//Start flask API server
function startApiServer() {
    return new Promise((resolve, reject) => {
        const pythonPath = process.platform === 'win32' ? 'python': 'python3';
        const apiScriptPath = join(__dirname, '..', 'api', 'app.py');

        apiProcess = spawn(pythonPath, [apiScriptPath]);

        apiProcess.stdout.on('data', (data) => {
            // console.log(`API: ${data}`);
            // if (data.toString().includes('Running on')) {
            //     resolve();
            // }
            const text = data.toString();
            console.log(`API: ${text}`);
            if (text.includes('FLASK_API_READY')|| text.includes('Running on')) {
            resolve();}
        });

        
        apiProcess.stderr.on('data', (data) => {
            console.error(`API Error: ${data}`);
        });

        apiProcess.on('close', (code) => {
            console.log(`API process exited with code ${code}`);
        })

        //timeout after 10 seconds
        setTimeout(() => {
            reject(new Error('API server failed to start within 10 seconds'));
        }, 10000);
    })
};

//check if API is running
async function waitForApi() {
    const maxAttempts = 30;
    for (let i = 0; i < maxAttempts; i++) {
        try {
            await get(`${API_URL}/health`);
            return true;
        } catch (error) {
            await new Promise(res => setTimeout(res, 1000));
        };
    };
    return false;
};

//app initialization
app.whenReady().then(
async() => {
    try {
        //start API server
        console.log('Starting API server...');
        await startApiServer();

        //wait for API to be running
        console.log('Waiting for API server to be ready...');
        const apiReady = await waitForApi();
        if (!apiReady) {
            throw new Error('API server failed to start');
        }
        console.log('API server is running.');

        //create main window
        createWindow();

        //show notification
        if (Notification.isSupported()) {
            new Notification({
                title: 'Electron App',
                body: 'Application is ready!',
                //icon: path.join(__dirname, 'assets', 'icon.png')
            }).show();
        }
    } catch (error) {
        console.error('Error during app initialization:', error);
        dialog.showErrorBox('Startup Error', `Failed to start application: ${error.message}`);
        app.quit();
    };
});

//handle all windows closed
app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        app.quit();
    }
});

app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
        createWindow();
    }
});

//cleanup on app quit
app.on('quit', () => {
    console.log('shutting down...');

    //kill API process
    if (apiProcess) {
        apiProcess.kill();
    }

    //kill bot process
    if (botProcess) {
        botProcess.kill();
    }
});


//IPC handlers can be added here
ipcMain.handle('get-api-url', () => API_URL);

ipcMain.handle('open-file-dialog', async () => {
    const result = await dialog.showOpenDialog(mainWindow, {
        properties: ['openFile'],
        filters:[
            {name: 'Images', extensions: ['jpg','jpeg', 'png','gif']},
            {name: 'videos', extensions: ['mp4', 'avi', 'mkv']},
            {name: 'All Files', extensions: ['*']}
        ]
    });

    if (!result.canceled && result.filePaths.length > 0) {
        const filePath = result.filePaths[0];
        const fileName = basename(filePath);
        const fileData = readFileSync(filePath);

        return {
            path: filePath,
            name: fileName,
            data: fileData.toString('base64'),
            size: fileData.length
        };
    }

    return null;
});

//show notification 
ipcMain.handle('show-notification', (event, {title, body}) => {
    if (Notification.isSupported()){
        new Notification({title, body}).show();
    }
});

//start bot process
ipcMain.handle('start-bot', async () => {
    try {
        const response = await post(`${API_URL}/api/bot/start`);
        return response.data;
    }catch(error){
        throw new Error(error.response?.data?.error || error.message);
    }
});

//stop bot
ipcMain.handle('stop-bot', async () => {
    try {
        const response = await post(`${API_URL}/api/bot/stop`);
        return response.data;
    }catch(error){
        throw new Error(error.response?.data?.error || error.message);
    }
});

//Backup data
ipcMain.handle('backup-data', async () => {
    try{
        const response = await post(`${API_URL}/api/backup`);
        return response.data;
    }catch(error){
        throw new Error(error.response?.data?.error || error.message);
    }
});