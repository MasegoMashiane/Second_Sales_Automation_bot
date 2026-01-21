import React, { useState, useEffect } from 'react';
import { BarChart, Bar, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { Activity, Mail, Facebook, Instagram, Linkedin, TrendingUp, Upload, Calendar, Settings, PlayCircle, PauseCircle, AlertCircle, CheckCircle, X, Plus, Download, RefreshCw } from 'lucide-react';

const AutomationDashboard = () => {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [botStatus, setBotStatus] = useState('running');
  const [showUploadModal, setShowUploadModal] = useState(false);
  const [uploadData, setUploadData] = useState({
    platform: 'Facebook',
    caption: '',
    hashtags: '',
    scheduleDate: '',
    scheduleTime: '',
    file: null,
    filePreview: null
  });
  const [scheduledPosts, setScheduledPosts] = useState([
    { id: 1, platform: 'Facebook', caption: 'Check out our new product!', date: '2025-12-08', time: '14:00', status: 'Pending', media: 'product.jpg' },
    { id: 2, platform: 'Instagram', caption: 'Behind the scenes', date: '2025-12-08', time: '16:00', status: 'Pending', media: 'bts.jpg' },
    { id: 3, platform: 'LinkedIn', caption: 'Industry insights', date: '2025-12-09', time: '09:00', status: 'Pending', media: null }
  ]);

  const [quotaData, setQuotaData] = useState({
    email: { used: 150, limit: 450, success: 148, failed: 2 },
    facebook: { used: 25, limit: 200, success: 25, failed: 0 },
    instagram: { used: 15, limit: 100, success: 14, failed: 1 },
    linkedin: { used: 30, limit: 100, success: 29, failed: 1 }
  });

  const [recentActivity, setRecentActivity] = useState([
    { time: '10:30 AM', type: 'Email', status: 'Success', details: 'Sent to john@example.com' },
    { time: '10:28 AM', type: 'Facebook', status: 'Success', details: 'Posted: "New product launch..."' },
    { time: '10:25 AM', type: 'LinkedIn', status: 'Success', details: 'Posted: "Excited to announce..."' }
  ]);

  const weeklyStats = [
    { day: 'Mon', emails: 45, posts: 8 },
    { day: 'Tue', emails: 52, posts: 9 },
    { day: 'Wed', emails: 48, posts: 7 },
    { day: 'Thu', emails: 61, posts: 10 },
    { day: 'Fri', emails: 38, posts: 6 },
    { day: 'Sat', emails: 12, posts: 4 },
    { day: 'Sun', emails: 8, posts: 3 }
  ];

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setUploadData({
        ...uploadData,
        file: file,
        filePreview: URL.createObjectURL(file)
      });
    }
  };

  const handleSubmitPost = async (e) => {
    e.preventDefault();
    
    if (!uploadData.caption || !uploadData.scheduleDate || !uploadData.scheduleTime) {
      alert('Please fill in all required fields');
      return;
    }

    if (uploadData.platform === 'Instagram' && !uploadData.file) {
      alert('Instagram requires an image or video');
      return;
    }

    const newPost = {
      id: scheduledPosts.length + 1,
      platform: uploadData.platform,
      caption: uploadData.caption,
      hashtags: uploadData.hashtags,
      date: uploadData.scheduleDate,
      time: uploadData.scheduleTime,
      status: 'Pending',
      media: uploadData.file ? uploadData.file.name : null
    };

    setScheduledPosts([...scheduledPosts, newPost]);

    setUploadData({
      platform: 'Facebook',
      caption: '',
      hashtags: '',
      scheduleDate: '',
      scheduleTime: '',
      file: null,
      filePreview: null
    });

    setShowUploadModal(false);
    alert('Post scheduled successfully!');
  };

  const handleDeletePost = (postId) => {
    if (window.confirm('Delete this scheduled post?')) {
      setScheduledPosts(scheduledPosts.filter(p => p.id !== postId));
    }
  };

  const getPlatformIcon = (platform) => {
    switch(platform) {
      case 'Facebook': return <Facebook />;
      case 'Instagram': return <Instagram />;
      case 'LinkedIn': return <Linkedin />;
      default: return null;
    }
  };

  const getPlatformColor = (platform) => {
    switch(platform) {
      case 'Facebook': return {backgroundColor: '#1877F2'};
      case 'Instagram': return {backgroundImage: 'linear-gradient(to right, #833AB4, #FD1D1D, #F77737)'};
      case 'LinkedIn': return {backgroundColor: '#0A66C2'};
      default: return {backgroundColor: '#858585'};
    }
  };

  const QuotaCard = ({ platform, icon: Icon, data }) => {
    const percentage = (data.used / data.limit * 100).toFixed(1);
    const statusColor = percentage > 80 ? '#dc2626' : percentage > 50 ? ' #d97706' : '#10b981';
    
    return (
      <div className="cards">
        <div className="container">
          <div className="containerelemets">
            <div className="iconContainer" style={getPlatformColor(platform)}>
              <Icon className="icon" />
            </div>
            <div>
              <h3 className="platformName">{platform}</h3>
              <p className="dailyQuota">Daily Quota</p>
            </div>
          </div>
          <span className="percentage" style={{ color: statusColor }}>{percentage}%</span>
        </div>
        
        <div className="ratioBarContainer">
          <div className="ratioContainer">
            <span className="ratio">{data.used} / {data.limit}</span>
          </div>
          <div className="bar">
            <div 
              className="fill"  
              style={{
                backgroundImage: percentage > 80 ? 'linear-gradient(to right, #ef4444, #dc2626)' : 
                  percentage > 50 ? 'linear-gradient(to right, #f59e0b, #d97706)' : 
                  'linear-gradient(to right, #62dab2, #025037)',
                width: `${percentage}%`
              }}
            />
          </div>
        </div>
        
        <div className="successFailureContainer">
          <span className="success">✓ {data.success}</span>
          <span className="failure">✗ {data.failed}</span>
        </div>
      </div>
    );
  };

  const UploadModal = () => (
    <div className="uploadSection">
      <div className="uploadContainer">
        <div className="schedulepostcontainer">
          <div className="scheduleitemscontainer">
            <div>
              <h2>Schedule New Post</h2>
              <p>Create and schedule your social media content</p>
            </div>
            <button onClick={() => setShowUploadModal(false)} className="setShowUploadModal">
              <X style={{ width: '1.5rem', height: '1.5rem' }} />
            </button>
          </div>
        </div>

        <form onSubmit={handleSubmitPost} className="p-6 space-y-6">
          {/* Platform Selection */}
          <div>
            <label className="block text-sm font-bold text-gray-700 mb-3">
              Platform <span className="text-[#620000]">*</span>
            </label>
            <div className="grid grid-cols-3 gap-3">
              {['Facebook', 'Instagram', 'LinkedIn'].map(platform => (
                <button
                  key={platform}
                  type="button"
                  onClick={() => setUploadData({...uploadData, platform})}
                  className={`p-4 border-2 rounded-xl flex flex-col items-center gap-2 transition-all duration-300 ${
                    uploadData.platform === platform 
                      ? `${getPlatformColor(platform)} border-transparent text-white shadow-lg transform scale-105` 
                      : 'border-gray-200 hover:border-[#620000] hover:shadow-md'
                  }`}
                >
                  {getPlatformIcon(platform)}
                  <span className="font-semibold text-sm">{platform}</span>
                </button>
              ))}
            </div>
          </div>

          {/* File Upload */}
          <div>
            <label className="block text-sm font-bold text-gray-700 mb-3">
              Upload Media {uploadData.platform === 'Instagram' && <span className="text-[#620000]">*</span>}
            </label>
            <div className="border-2 border-dashed border-gray-300 rounded-xl p-8 hover:border-[#620000] transition-colors bg-gray-50">
              {uploadData.filePreview ? (
                <div className="relative">
                  <img 
                    src={uploadData.filePreview} 
                    alt="Preview" 
                    className="max-h-64 mx-auto rounded-xl shadow-lg"
                  />
                  <button
                    type="button"
                    onClick={() => setUploadData({...uploadData, file: null, filePreview: null})}
                    className="absolute top-2 right-2 p-2 bg-[#620000] text-white rounded-full hover:bg-[#8B0000] shadow-lg transition-colors"
                  >
                    <X className="w-4 h-4" />
                  </button>
                </div>
              ) : (
                <div className="text-center">
                  <Upload className="w-16 h-16 text-gray-400 mx-auto mb-4" />
                  <label className="cursor-pointer">
                    <span className="text-[#620000] hover:text-[#8B0000] font-bold text-lg">
                      Click to upload
                    </span>
                    <span className="text-gray-600"> or drag and drop</span>
                    <input
                      type="file"
                      accept="image/*,video/*"
                      onChange={handleFileChange}
                      className="hidden"
                    />
                  </label>
                  <p className="text-sm text-gray-500 mt-2">PNG, JPG, MP4 up to 10MB</p>
                </div>
              )}
            </div>
          </div>

          {/* Caption */}
          <div>
            <label className="block text-sm font-bold text-gray-700 mb-3">
              Caption <span className="text-[#620000]">*</span>
            </label>
            <textarea
              value={uploadData.caption}
              onChange={(e) => setUploadData({...uploadData, caption: e.target.value})}
              rows={4}
              className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:ring-2 focus:ring-[#620000] focus:border-transparent resize-none transition-all"
              placeholder="Write your caption here..."
              required
            />
            <p className="text-sm text-gray-500 mt-2 font-medium">{uploadData.caption.length} characters</p>
          </div>

          {/* Hashtags */}
          <div>
            <label className="block text-sm font-bold text-gray-700 mb-3">
              Hashtags
            </label>
            <input
              type="text"
              value={uploadData.hashtags}
              onChange={(e) => setUploadData({...uploadData, hashtags: e.target.value})}
              className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:ring-2 focus:ring-[#620000] focus:border-transparent transition-all"
              placeholder="#marketing #business #success"
            />
          </div>

          {/* Schedule Date & Time */}
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-bold text-gray-700 mb-3">
                Date <span className="text-[#620000]">*</span>
              </label>
              <input
                type="date"
                value={uploadData.scheduleDate}
                onChange={(e) => setUploadData({...uploadData, scheduleDate: e.target.value})}
                className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:ring-2 focus:ring-[#620000] focus:border-transparent transition-all"
                required
                min={new Date().toISOString().split('T')[0]}
              />
            </div>
            <div>
              <label className="block text-sm font-bold text-gray-700 mb-3">
                Time <span className="text-[#620000]">*</span>
              </label>
              <input
                type="time"
                value={uploadData.scheduleTime}
                onChange={(e) => setUploadData({...uploadData, scheduleTime: e.target.value})}
                className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:ring-2 focus:ring-[#620000] focus:border-transparent transition-all"
                required
              />
            </div>
          </div>

          {/* Submit Buttons */}
          <div className="flex gap-3 pt-4">
            <button
              type="submit"
              className="flex-1 px-6 py-4 bg-gradient-to-r from-[#620000] to-[#8B0000] text-white rounded-xl hover:from-[#8B0000] hover:to-[#620000] font-bold flex items-center justify-center gap-2 shadow-lg hover:shadow-xl transition-all transform hover:scale-105"
            >
              <Calendar className="w-5 h-5" />
              Schedule Post
            </button>
            <button
              type="button"
              onClick={() => setShowUploadModal(false)}
              className="px-6 py-4 border-2 border-gray-300 text-gray-700 rounded-xl hover:bg-gray-50 font-bold transition-all"
            >
              Cancel
            </button>
          </div>
        </form>
      </div>
    </div>
  );

  const DashboardTab = () => (
    <div className="space-y-6">
      {/* Status Banner */}
      <div className={`p-6 rounded-2xl shadow-lg ${botStatus === 'running' ? 'bg-gradient-to-r from-emerald-50 to-emerald-100 border-2 border-emerald-200' : 'bg-gradient-to-r from-red-50 to-red-100 border-2 border-red-200'}`}>
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-4">
            {botStatus === 'running' ? (
              <div className="p-3 bg-emerald-500 rounded-xl shadow-lg">
                <CheckCircle className="w-8 h-8 text-white" />
              </div>
            ) : (
              <div className="p-3 bg-red-500 rounded-xl shadow-lg">
                <AlertCircle className="w-8 h-8 text-white" />
              </div>
            )}
            <div>
              <h3 className="text-xl font-bold text-gray-800">
                Bot Status: {botStatus === 'running' ? 'Running' : 'Stopped'}
              </h3>
              <p className="text-sm text-gray-600 font-medium">
                {botStatus === 'running' ? 'All systems operational' : 'Bot is currently stopped'}
              </p>
            </div>
          </div>
          <button
            onClick={() => setBotStatus(botStatus === 'running' ? 'stopped' : 'running')}
            className={`px-6 py-3 rounded-xl font-bold flex items-center gap-2 shadow-lg hover:shadow-xl transition-all transform hover:scale-105 ${
              botStatus === 'running' 
                ? 'bg-gradient-to-r from-red-500 to-red-600 hover:from-red-600 hover:to-red-700 text-white' 
                : 'bg-gradient-to-r from-emerald-500 to-emerald-600 hover:from-emerald-600 hover:to-emerald-700 text-white'
            }`}
          >
            {botStatus === 'running' ? (
              <>
                <PauseCircle className="w-5 h-5" />
                Stop Bot
              </>
            ) : (
              <>
                <PlayCircle className="w-5 h-5" />
                Start Bot
              </>
            )}
          </button>
        </div>
      </div>

      {/* Quota Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <QuotaCard platform="Email" icon={Mail} data={quotaData.email} color="bg-gradient-to-br from-[#620000] to-[#8B0000]" />
        <QuotaCard platform="Facebook" icon={Facebook} data={quotaData.facebook} color="bg-[#1877F2]" />
        <QuotaCard platform="Instagram" icon={Instagram} data={quotaData.instagram} color="bg-gradient-to-br from-[#833AB4] via-[#FD1D1D] to-[#F77737]" />
        <QuotaCard platform="LinkedIn" icon={Linkedin} data={quotaData.linkedin} color="bg-[#0A66C2]" />
      </div>

      {/* Charts */}
      <div className="bg-white rounded-2xl shadow-lg p-8 border border-gray-100">
        <h3 className="text-xl font-bold mb-6 flex items-center gap-3 text-gray-800">
          <div className="p-2 bg-gradient-to-br from-[#620000] to-[#8B0000] rounded-lg">
            <TrendingUp className="w-6 h-6 text-white" />
          </div>
          Weekly Activity
        </h3>
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={weeklyStats}>
            <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
            <XAxis dataKey="day" stroke="#666" />
            <YAxis stroke="#666" />
            <Tooltip 
              contentStyle={{ 
                backgroundColor: '#fff', 
                border: '2px solid #620000',
                borderRadius: '12px',
                padding: '12px'
              }}
            />
            <Legend />
            <Line type="monotone" dataKey="emails" stroke="#620000" strokeWidth={3} dot={{ fill: '#620000', r: 5 }} />
            <Line type="monotone" dataKey="posts" stroke="#10b981" strokeWidth={3} dot={{ fill: '#10b981', r: 5 }} />
          </LineChart>
        </ResponsiveContainer>
      </div>

      {/* Recent Activity */}
      <div className="bg-white rounded-2xl shadow-lg p-8 border border-gray-100">
        <h3 className="text-xl font-bold mb-6 flex items-center gap-3 text-gray-800">
          <div className="p-2 bg-gradient-to-br from-[#620000] to-[#8B0000] rounded-lg">
            <Activity className="w-6 h-6 text-white" />
          </div>
          Recent Activity
        </h3>
        <div className="space-y-3">
          {recentActivity.map((activity, idx) => (
            <div key={idx} className="flex items-center justify-between p-4 bg-gray-50 rounded-xl hover:bg-gray-100 transition-all border border-gray-100">
              <div className="flex items-center gap-4">
                <span className="text-sm text-gray-500 font-medium w-20">{activity.time}</span>
                <span className={`px-4 py-2 rounded-lg text-sm font-bold ${
                  activity.type === 'Email' ? 'bg-[#620000] text-white' :
                  activity.type === 'Facebook' ? 'bg-[#1877F2] text-white' :
                  activity.type === 'Instagram' ? 'bg-gradient-to-r from-[#833AB4] to-[#FD1D1D] text-white' :
                  'bg-[#0A66C2] text-white'
                }`}>
                  {activity.type}
                </span>
                <span className="text-sm text-gray-700 font-medium">{activity.details}</span>
              </div>
              <span className={`px-4 py-2 rounded-lg text-sm font-bold ${
                activity.status === 'Success' ? 'bg-emerald-100 text-emerald-700' : 'bg-red-100 text-red-700'
              }`}>
                {activity.status}
              </span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );

  const ScheduleTab = () => (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-3xl font-bold text-gray-900">Scheduled Posts</h2>
          <p className="text-gray-600 mt-1">Manage your social media content calendar</p>
        </div>
        <button
          onClick={() => setShowUploadModal(true)}
          className="px-8 py-4 bg-gradient-to-r from-[#620000] to-[#8B0000] text-white rounded-xl hover:from-[#8B0000] hover:to-[#620000] font-bold flex items-center gap-3 shadow-lg hover:shadow-xl transition-all transform hover:scale-105"
        >
          <Plus className="w-6 h-6" />
          New Post
        </button>
      </div>

      {/* Scheduled Posts List */}
      <div className="space-y-4">
        {scheduledPosts.map(post => (
          <div key={post.id} className="bg-white rounded-2xl shadow-lg hover:shadow-xl transition-all p-6 border border-gray-100">
            <div className="flex items-start justify-between">
              <div className="flex gap-6 flex-1">
                {/* Platform Icon */}
                <div className={`p-4 rounded-xl ${getPlatformColor(post.platform)} shadow-md`}>
                  {getPlatformIcon(post.platform)}
                </div>

                {/* Post Details */}
                <div className="flex-1">
                  <div className="flex items-center gap-3 mb-3">
                    <h3 className="font-bold text-lg text-gray-900">{post.platform}</h3>
                    <span className={`px-4 py-1 rounded-full text-sm font-bold ${
                      post.status === 'Pending' ? 'bg-amber-100 text-amber-700' :
                      post.status === 'Posted' ? 'bg-emerald-100 text-emerald-700' :
                      'bg-red-100 text-red-700'
                    }`}>
                      {post.status}
                    </span>
                  </div>
                  <p className="text-gray-700 mb-3 font-medium">{post.caption}</p>
                  {post.hashtags && (
                    <p className="text-[#620000] text-sm mb-3 font-semibold">{post.hashtags}</p>
                  )}
                  <div className="flex items-center gap-6 text-sm text-gray-500">
                    <span className="flex items-center gap-2 font-medium">
                      <Calendar className="w-4 h-4" />
                      {post.date} at {post.time}
                    </span>
                    {post.media && (
                      <span className="flex items-center gap-2 font-medium">
                        <Upload className="w-4 h-4" />
                        {post.media}
                      </span>
                    )}
                  </div>
                </div>
              </div>

              {/* Actions */}
              <button
                onClick={() => handleDeletePost(post.id)}
                className="p-3 text-red-600 hover:bg-red-50 rounded-xl transition-all"
              >
                <X className="w-6 h-6" />
              </button>
            </div>
          </div>
        ))}
      </div>

      {scheduledPosts.length === 0 && (
        <div className="text-center py-20 bg-white rounded-2xl shadow-lg border-2 border-dashed border-gray-300">
          <Upload className="w-20 h-20 text-gray-400 mx-auto mb-6" />
          <h3 className="text-2xl font-bold text-gray-900 mb-3">No scheduled posts</h3>
          <p className="text-gray-600 mb-8 text-lg">Get started by scheduling your first post</p>
          <button
            onClick={() => setShowUploadModal(true)}
            className="px-8 py-4 bg-gradient-to-r from-[#620000] to-[#8B0000] text-white rounded-xl hover:from-[#8B0000] hover:to-[#620000] font-bold inline-flex items-center gap-3 shadow-lg hover:shadow-xl transition-all"
          >
            <Plus className="w-6 h-6" />
            Schedule Post
          </button>
        </div>
      )}
    </div>
  );

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100">
      {/* Header */}
      <header className="bg-gradient-to-r from-[#620000] to-[#8B0000] text-white shadow-2xl">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <div className="p-3 bg-white/20 rounded-xl backdrop-blur-sm">
                <Activity className="w-8 h-8 text-white" />
              </div>
              <div>
                <h1 className="text-3xl font-bold">Sales Automation</h1>
                <p className="text-sm text-white/90 mt-1">Multi-Platform Campaign Manager</p>
              </div>
            </div>
            <div className="flex items-center gap-3">
              <button className="p-3 bg-white/20 rounded-xl hover:bg-white/30 transition-all backdrop-blur-sm">
                <RefreshCw className="w-5 h-5" />
              </button>
              <button className="p-3 bg-white/20 rounded-xl hover:bg-white/30 transition-all backdrop-blur-sm">
                <Download className="w-5 h-5" />
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Navigation */}
      <nav className="bg-white border-b border-gray-200 shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex gap-8">
            {[
              { id: 'dashboard', label: 'Dashboard', icon: Activity },
              { id: 'schedule', label: 'Schedule Posts', icon: Calendar },
              { id: 'settings', label: 'Settings', icon: Settings }
            ].map(tab => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex items-center gap-3 px-6 py-4 border-b-4 font-bold transition-all ${
                  activeTab === tab.id
                    ? 'border-[#620000] text-[#620000]'
                    : 'border-transparent text-gray-600 hover:text-gray-900 hover:border-gray-300'
                }`}
              >
                <tab.icon className="w-5 h-5" />
                {tab.label}
              </button>
            ))}
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {activeTab === 'dashboard' && <DashboardTab />}
        {activeTab === 'schedule' && <ScheduleTab />}
        {activeTab === 'settings' && (
          <div className="space-y-6">
            <div>
              <h2 className="text-3xl font-bold text-gray-900">Settings</h2>
              <p className="text-gray-600 mt-1">Configure your automation preferences</p>
            </div>

            {/* Bot Controls */}
            <div className="bg-white rounded-2xl shadow-lg p-8 border border-gray-100">
              <h3 className="text-xl font-bold mb-6 flex items-center gap-3 text-gray-800">
                <div className="p-2 bg-gradient-to-br from-[#620000] to-[#8B0000] rounded-lg">
                  <Settings className="w-6 h-6 text-white" />
                </div>
                Bot Controls
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <button className="p-6 bg-gradient-to-r from-emerald-500 to-emerald-600 text-white rounded-xl hover:from-emerald-600 hover:to-emerald-700 font-bold flex items-center justify-center gap-3 shadow-lg hover:shadow-xl transition-all transform hover:scale-105">
                  <PlayCircle className="w-6 h-6" />
                  Start Bot
                </button>
                <button className="p-6 bg-gradient-to-r from-red-500 to-red-600 text-white rounded-xl hover:from-red-600 hover:to-red-700 font-bold flex items-center justify-center gap-3 shadow-lg hover:shadow-xl transition-all transform hover:scale-105">
                  <PauseCircle className="w-6 h-6" />
                  Stop Bot
                </button>
                <button className="p-6 bg-gradient-to-r from-[#620000] to-[#8B0000] text-white rounded-xl hover:from-[#8B0000] hover:to-[#620000] font-bold flex items-center justify-center gap-3 shadow-lg hover:shadow-xl transition-all transform hover:scale-105">
                  <Download className="w-6 h-6" />
                  Backup Data
                </button>
              </div>
            </div>

            {/* Daily Limits */}
            <div className="bg-white rounded-2xl shadow-lg p-8 border border-gray-100">
              <h3 className="text-xl font-bold mb-6 text-gray-800">Daily Limits</h3>
              <div className="space-y-4">
                {Object.entries(quotaData).map(([platform, data]) => (
                  <div key={platform} className="flex items-center justify-between p-4 bg-gray-50 rounded-xl border border-gray-100">
                    <span className="capitalize font-bold text-gray-700">{platform}</span>
                    <div className="flex items-center gap-4">
                      <input
                        type="number"
                        value={data.limit}
                        className="w-24 px-4 py-2 border-2 border-gray-200 rounded-lg font-medium focus:ring-2 focus:ring-[#620000] focus:border-transparent"
                        readOnly
                      />
                      <span className="text-sm text-gray-500 font-medium">per day</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}
      </main>

      {/* Upload Modal */}
      {showUploadModal && <UploadModal />}
    </div>
  );
};

export default AutomationDashboard;