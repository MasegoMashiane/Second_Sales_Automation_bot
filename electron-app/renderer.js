const { ipcRenderer } = window.electron; 

let API_URL;
//Initialize
window.addEventListener('DOMContentLoaded', async () => {
    API_URL = await window.electronAPI.getAPIURL();
    loadDashboard();
    loadScheduledPosts();
    //Auto-refresh dashboard every 30 seconds
    setInterval(loadDashboard, 30000);
});

//Tab switching
function switchTab(tabName, event) {
    //hide all tabs
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.add('hidden');
    });

    //show selected tab
    document.getElementById(`${tabName}-tab`).classList.remove('hidden');

    //update tab buttons
    document.querySelectorAll('.tab-button').forEach(btn => {
        btn.classList.remove('border-blue-500', 'text-blue-600');
        btn.classList.add('border-transparent', 'text-gray-600');
    });

    event.target.classList.add('border-blue-500', 'text-blue-600');
    event.target.classList.remove('border-transparent', 'text-gray-600');
};

//Load dashboard data
async function loadDashboard() {
    try {
        const response = await fetch(`${API_URL}/api/quotas`);
        
        if (!response.ok){
        throw new Error(`API Error: ${response.status}`);
        }

        const quotas = await response.json();


        //update quota displays
        document.getElementById('email-used').textContent = quotas.email.used;
        document.getElementById('email-limit').textContent = quotas.email.limit;
        document.getElementById('fb-used').textContent = quotas.facebook.used;
        document.getElementById('fb-limit').textContent = quotas.facebook.limit;
        document.getElementById('ig-used').textContent = quotas.Instagram.used;
        document.getElementById('ig-limit').textContent = quotas.Instagram.limit;
        
        //load recent activities
        const activitiesResponse = await fetch(`${API_URL}/api/activity/recent?limit=10`);
        const activities = await activitiesResponse.json();

        const activitiesList = document.getElementById('recent-activities-list');
        activitiesList.innerHTML = activities.map( a => {
            return `<div class="p-3 bg-gray-50 rounded flex justify-between items-center">
                        <div>
                    <span class="text-sm text-gray-500">${a.time}</span>
                    <span class="ml-3 font-medium">${a.type}</span>
                    <span class="ml-2 text-sm text-gray-600">${a.details}</span>
                </div>
                <span class="px-3 py-1 rounded-full text-sm ${a.status === 'Success' ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'}">
                    ${a.status}
                </span>
            </div>`}).join('');       
    }
    catch (error) {
        console.error('Error loading dashboard:', error);
    }
};

//Load scheduled posts
async function loadScheduledPosts() {
    try {
        const response = await fetch(`${API_URL}/api/posts`);
        const posts = await response.json();
        
        const postsList = document.getElementById('posts-list');
        postsList.innerHTML = posts.map(post => `
            <div class="bg-white p-6 rounded-lg shadow">
                <div class="flex justify-between">
                    <div class="flex-1">
                        <div class="flex items-center gap-2 mb-2">
                            <span class="px-3 py-1 rounded-full text-sm font-medium ${
                                post.platform === 'Facebook' ? 'bg-blue-100 text-blue-700' :
                                post.platform === 'Instagram' ? 'bg-pink-100 text-pink-700' :
                                'bg-blue-100 text-blue-800'
                            }">${post.platform}</span>
                            <span class="px-3 py-1 rounded-full text-sm font-medium ${
                                post.status === 'Pending' ? 'bg-yellow-100 text-yellow-700' :
                                'bg-green-100 text-green-700'
                            }">${post.status}</span>
                        </div>
                        <p class="font-medium mb-2">${post.caption}</p>
                        <p class="text-sm text-gray-600">${post.date} at ${post.time}</p>
                        ${post.media ? `<p class="text-sm text-gray-500 mt-1">📎 ${post.media}</p>` : ''}
                    </div>
                    <button onclick="deletePost(${post.id})" class="text-red-600 hover:text-red-800">
                        Delete
                    </button>
                </div>
            </div>
        `).join('');
        
    } catch (error) {
        console.error('Error loading posts:', error);
    }
};

//bot controls
async function startBot() {
    try {
        const result = await window.electronAPI.startBot();
        await window.electronAPI.showNotification({
            title: 'Bot Started',
            body: 'Automation bot is now running'
        });
        loadDashboard();
    } catch (error) {
        alert('Error starting bot: ' + error.message);
    }
}

async function stopBot() {
    try {
        const result = await window.electronAPI.stopBot();
        await window.electronAPI.showNotification('Bot Stopped', 'Automation bot has been stopped');
        loadDashboard();
    } catch (error) {
        alert('Error stopping bot: ' + error.message);
    }
}

async function backupData() {
    try {
        const result = await window.electronAPI.backupData();
        await window.electronAPI.showNotification('Backup Complete', 'Data backed up successfully');
    } catch (error) {
        alert('Error backing up data: ' + error.message);
    }
}

//Modal Functions
function showUploadModal() {
    document.getElementById('upload-modal').classList.remove('hidden');
    buildUploadForm();
}

function hideUploadModal() {
    document.getElementById('upload-modal').classList.add('hidden');
}

//build upload form
function buildUploadForm() {
    const form = document.getElementById('upload-form');
    form.innerHTML = ` 
    <!-- Platform Selection -->
        <div>
            <label class="block font-medium mb-2">Platform *</label>
            <select id="platform" required class="w-full px-4 py-2 border rounded-lg">
                <option value="Facebook">Facebook</option>
                <option value="Instagram">Instagram</option>
                <option value="LinkedIn">LinkedIn</option>
            </select>
        </div>
        
        <!-- File Upload -->
        <div>
            <label class="block font-medium mb-2">Upload Media</label>
            <button type="button" onclick="selectFile()" 
                    class="w-full px-4 py-3 border-2 border-dashed rounded-lg hover:border-blue-500 transition-colors">
                Click to select file
            </button>
            <div id="file-preview" class="mt-3 hidden">
                <img id="preview-image" class="max-h-48 rounded-lg mx-auto">
                <p id="file-name" class="text-sm text-gray-600 mt-2 text-center"></p>
            </div>
        </div>
        
        <!-- Caption -->
        <div>
            <label class="block font-medium mb-2">Caption *</label>
            <textarea id="caption" required rows="4" 
                      class="w-full px-4 py-2 border rounded-lg resize-none"
                      placeholder="Write your caption..."></textarea>
        </div>
        
        <!-- Hashtags -->
        <div>
            <label class="block font-medium mb-2">Hashtags</label>
            <input type="text" id="hashtags" 
                   class="w-full px-4 py-2 border rounded-lg"
                   placeholder="#marketing #business">
        </div>
        
        <!-- Date & Time -->
        <div class="grid grid-cols-2 gap-4">
            <div>
                <label class="block font-medium mb-2">Date *</label>
                <input type="date" id="scheduleDate" required 
                       class="w-full px-4 py-2 border rounded-lg"
                       min="${new Date().toISOString().split('T')[0]}">
            </div>
            <div>
                <label class="block font-medium mb-2">Time *</label>
                <input type="time" id="scheduleTime" required 
                       class="w-full px-4 py-2 border rounded-lg">
            </div>
        </div>
        
        <!-- Submit Button -->
        <button type="submit" 
                class="w-full px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 font-medium">
            Schedule Post
        </button>
    `;
    
    form.onsubmit = handleSubmitPost;
}

let selectedFile = null;

//ifner Mime type to avoid breaks
function getMimeType(filename) {
    const ext = filename.split('.').pop().toLowerCase();
    return{
        'jpg': 'image/jpeg',
        'jpeg': 'image/jpeg',
        'png': 'image/png',
        'gif': 'image/gif',
        'mp4': 'video/mp4',
        'avi': 'video/x-msvideo',
        'mkv': 'video/x-matroska'
    }[ext] || 'application/octet-stream';
}

//File selection
async function selectFile() {
   const file = await window.electronAPI.openFileDialog();
   if (file) {
       selectedFile = file;

       //show preview
       const previewDiv = document.getElementById('file-preview');
       const previewImage = document.getElementById('preview-image');
       const fileName = document.getElementById('file-name');
       
       previewDiv.classList.remove('hidden');

        //Convert base64 to blob URL for preview
        let mime = getMimeType(file.name);
        const blob = base64ToBlob(file.data, mime);
        const blobURL = URL.createObjectURL(blob);
        previewImage.src = blobURL;

        fileName.textContent = file.name;
    }
}

//convert base64 to blob
function base64ToBlob(base64, type){
    const byteCharacters = atob(base64);
    const byteNumbers = new Array(byteCharacters.length);
    for (let i = 0; i < byteCharacters.length; i++) {
        byteNumbers[i] = byteCharacters.charCodeAt(i);
    }
    const byteArray = new Uint8Array(byteNumbers);
    return new Blob([byteArray], { type });
}

//submit post
async function handleSubmitPost(event) {
    event.preventDefault();

    const formData = new FormData();
    formData.append('platform', document.getElementById('platform').value);
    formData.append('caption', document.getElementById('caption').value);
    formData.append('hashtags', document.getElementById('hashtags').value);
    formData.append('scheduleDate', document.getElementById('scheduleDate').value);
    formData.append('scheduleTime', document.getElementById('scheduleTime').value);

    if(selectedFile) {
        //Convert base64 back to file
        const blob = base64ToBlob(selectedFile.data, 'image/jpeg');
        formData.append('file', blob, selectedFile.name);
    }

    try{
        const response = await fetch(`${API_URL}/api/posts`, {
            method: 'POST',
            body: formData
        })

        if (!response.ok) {
            throw new Error(`API Error: ${response.status}`);
        }
        const result = await response.json();

        if(response.ok){
            await window.electronAPI.showNotification('Success', 'Your post has been scheduled successfully');
            hideUploadModal();
            selectedFile = null;
            loadScheduledPosts();
        } else{
            alert('Error scheduling post: ' + result.message);
        }
    } catch (error) {
        alert('Error scheduling post: ' + error.message);
    }
}

//delete post
async function deletePost(postId) {
    if(!confirm('Are you sure you want to delete this post?')) return;
    try {
        await fetch(`${API_URL}/api/posts/${postId}`, {
            method: 'DELETE'
        });
        await window.electronAPI.showNotification('Deleted', 'The post has been deleted');
        loadScheduledPosts();
    } catch (error) {
        alert('Error deleting post: ' + error.message);
    }
};


window.showUploadModal = showUploadModal;
window.hideUploadModal = hideUploadModal;
window.switchTab = switchTab;
window.startBot = startBot;
window.stopBot = stopBot;
window.backupData = backupData;
window.selectFile = selectFile;
window.deletePost = deletePost;
window.handleSubmitPost = handleSubmitPost;
window.loadDashboard = loadDashboard;
window.loadScheduledPosts = loadScheduledPosts;