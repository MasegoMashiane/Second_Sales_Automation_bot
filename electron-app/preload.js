const { contextBridge, ipcRenderer } = require("electron")

contextBridge.exposeInMainWorld('electron', {
    ipcRenderer
});
//Expose protected methods
contextBridge.exposeInMainWorld('electronAPI', {
    //File operations
    openFileDialog: () => ipcRenderer.invoke('open-file-dialog'),

    //Noifications
    showNotification: (title, body) => ipcRenderer.invoke('show-notification', { title, body }),

    //API 
    getAPIURL: () => ipcRenderer.invoke('get-api-url'),

    //Bot controls
    startBot: () => ipcRenderer.invoke('start-bot'),
    stopBot: () => ipcRenderer.invoke('stop-bot'),
    backupData: () => ipcRenderer.invoke('backup-data')

});

