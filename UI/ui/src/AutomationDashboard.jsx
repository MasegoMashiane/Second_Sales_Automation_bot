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

  const getPlatformStyle = (platform, active) => {
    if (!active){
      return{
        borderColor: '#e5e7eb',
        color: '#aab4ca',
        boxShadow: '2px 5px 7px rgba(0, 0, 0, 0.05)',
        transform: 'scale(1)',
      }
    }

    let backgroundColor;
    switch(platform) {
      
      case 'Instagram':
      return{backgroundImage: 'linear-gradient(123deg, #833AB4, #FD1D1D, #F77737)',
              color: '#ffffff',borderColor: 'transparent',boxShadow: '0 10px 15px 3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)',
              transform: 'scale(1)'
            };
      
      case 'Facebook':
      return{backgroundColor:'#1877F2',color: '#ffffff',borderColor: 'transparent', boxShadow: '0 10px 15px 3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)',
              transform: 'scale(1)'};
      
      case 'LinkedIn':
      return{backgroundColor: '#0A66C2', color: '#ffffff',borderColor: 'transparent', boxShadow: '0 10px 15px 3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)',
              transform: 'scale(1)'};
      
      default: backgroundColor = '#858585';
    }
  }

  const QuotaCard = ({ platform, icon: Icon, data }) => {
    const percentage = (data.used / data.limit * 100).toFixed(1);
    const statusColor = percentage > 80 ? '#dc2626' : percentage > 50 ? ' #d97706' : '#10b981';
    
    return (
      <div className={`cards ${platform}card`}>
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

        <form onSubmit={handleSubmitPost} className="formContainer">
          <div>
            <label>
              Platform <span style={{color: '#ff0505'}}>*</span>
            </label>
            <div className="socialPlatformOptions">
              

              {['Facebook', 'Instagram', 'LinkedIn'].map(platform => (
                
                <button
                  id='PlatformButton'
                  key={platform}
                  type="button"
                  onClick={() => setUploadData({...uploadData, platform})}
                  style={{
                    padding: '1rem',
                    borderWidth: '2px',
                    borderStyle: 'solid',
                    borderRadius: '0.75rem',

                    display: 'flex',
                    flexDirection: 'column',
                    alignItems: 'center',
                    gap: '0.5rem',

                    cursor: 'pointer',
                    transition: 'all 300s ease',

                    ...getPlatformStyle(uploadData.platform, uploadData.platform === platform),
          
                  }}
                
                >
                  
                  {getPlatformIcon(platform)}
                  <span className="font-semibold text-sm">{platform}</span>

                </button>
              ))}
            </div>
          </div>

          {/* File Upload */}
          <div>
            <label className="fileUploadLabel">
              Upload Media {uploadData.platform === 'Instagram' && <span style={{color: '#ff0505'}}>*</span>}
            </label>
            <div className="UploadContainer">
              {uploadData.filePreview ? (
                <div className="relative">
                  <img 
                    src={uploadData.filePreview} 
                    alt="Preview" 
                    style={{maxHeight: '64rem', marginLeft: 'auto', marginRight: 'auto', borderRadius: '0.75rem', boxShadow: '0 10px 15px rgba(0, 0, 0, 0.1)'}}
                  
                  />
                  <button
                    type="button"
                    onClick={() => setUploadData({...uploadData, file: null, filePreview: null})}

                    style={{position: 'absolute', 
                      top: '0.5rem',
                      right: '0.5rem', 
                      padding: '0.5rem', 
                      backgroundColor: '#620000', 
                      color: '#ffffff', 
                      borderRadius: '9999px', 
                      hoverBackgroundColor: '#8B0000', 
                      boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)', 
                      transition: 'background-color 0.3s ease'}}
                    >
                    <X style={{width: '1rem', height: '1rem'}} />
                  </button>
                </div>
              ) : (
                <div className="UploadPlaceholder">
                  <Upload style={{width: '4rem', height: '4rem', marginLeft: 'auto', marginRight: 'auto', marginBottom: '1rem'}}
                  />
                  <label className="cursor-pointer">
                    <span
                    className="clickToUploadText">
                      Click to upload
                    </span>
                    <span style={{color: '#575757'}}> or drag and drop</span>
                    <input
                      type="file"
                      accept="image/*,video/*"
                      onChange={handleFileChange}
                      className="hidden"
                    />
                  </label>
                  <p style={{fontSize: '0.875rem', color: '#575757', marginTop: '0.5rem'}}>PNG, JPG, MP4 up to 10MB</p>
                </div>
              )}
            </div>
          </div>

          {/* Caption */}
          <div className='captionContainer'>
            <label className='caption'>
              Caption <span style={{color: '#ff0505'}}>*</span>
            </label>
            <textarea
              value={uploadData.caption}
              onChange={(e) => setUploadData({...uploadData, caption: e.target.value})}
              rows={4}
              placeholder="Write your caption here..."
              required
            />
            <p>{uploadData.caption.length} characters</p>
          </div>

          {/* Hashtags */}
          <div className='Hashtags'>
            <label>
              Hashtags
            </label>
            <input
              type="text"
              value={uploadData.hashtags}
              onChange={(e) => setUploadData({...uploadData, hashtags: e.target.value})}
              placeholder="#marketing #business #success"
            />
          </div>

          {/* Schedule Date & Time */}
          <div className="scheduleDateTimeContainer">
            <div>
              <label>
                Date <span style={{color: '#ff0505'}}>*</span>
              </label>
              <input
                type="date"
                value={uploadData.scheduleDate}
                onChange={(e) => setUploadData({...uploadData, scheduleDate: e.target.value})}
                required
                min={new Date().toISOString().split('T')[0]}
              />
            </div>
            <div>
              <label>
                Time <span style={{color: '#ff0505'}}>*</span>
              </label>
              <input
                type="time"
                value={uploadData.scheduleTime}
                onChange={(e) => setUploadData({...uploadData, scheduleTime: e.target.value})}
                required
              />
            </div>
          </div>

          {/* Submit Buttons */}
          <div className="submitCancelButtonsContainer">
            <button
              type="submit"
              id='submitButton'
            >
              <Calendar className="w-5 h-5" />
              Schedule Post
            </button>
            <button
              type="button"
              onClick={() => setShowUploadModal(false)}
              id='cancelButton'
            >Cancel
            </button>
          </div>
        </form>
      </div>
    </div>
  );

  const DashboardTab = () => (
    <div className="DashboardContainer">
      {/* Status Banner */}
      <div className={`status-card ${botStatus === 'running' ? 'running': 'stopped'}`}>
        <div className="statusBannerContainer">
          <div className="statusBannerContent">
            {botStatus === 'running' ? (
              <div className="statusIndicatorCheck">
                <CheckCircle style={{width: '2rem', height: '2rem', color: '#ffffff'}} />
              </div>
            ) : (
              <div style={{padding: '0.75rem', color:'#5a0707' ,backgroundColor: '#ef4444', borderRadius: '2rem', boxShadow: '0 4px 6px rgba(0,0,0,0.1)'}}>
                <AlertCircle className="w-8 h-8 text-white" />
              </div>
            )}
            <div>
              <h3 className={`statusTitle ${botStatus === 'running' ? 'runningText' : 'stoppedText'}  `}>
                Bot Status: {botStatus === 'running' ? 'Running' : 'Stopped'}
              </h3>
              <p className={`statusMessage ${botStatus === 'running' ? 'runningText' : 'stoppedText'}`}>
                {botStatus === 'running' ? 'All systems operational' : 'Bot is currently stopped'}
              </p>
            </div>
          </div>
          <button
            onClick={() => setBotStatus(botStatus === 'running' ? 'stopped' : 'running')}
            className={`bot-toggle-button ${
              botStatus === 'running' 
                ? 'running' 
                : 'stopped'
            }`}
          >
            {botStatus === 'running' ? (
              <>
                <PauseCircle style={{width: '1.25rem', height: '1.25rem'}} />
                Stop Bot
              </>
            ) : (
              <>
                <PlayCircle style={{width: '1.25rem', height: '1.25rem'}} />
                Start Bot
              </>
            )}
          </button>
        </div>
      </div>

      {/* Quota Cards */}
      <div className="quotaCards">
        <QuotaCard platform="Email" icon={Mail} data={quotaData.email}/>
        <QuotaCard platform="Facebook" icon={Facebook} data={quotaData.facebook} />
        <QuotaCard platform="Instagram" icon={Instagram} data={quotaData.instagram} />
        <QuotaCard platform="LinkedIn" icon={Linkedin} data={quotaData.linkedin}/>
      </div>

      {/* Charts */}
      <div className="chartContainer">
        <h3 className="chartTitle">
          <div>
            <TrendingUp style={{width: '1.5rem', height: '1.5rem', color: '#ffffff'}} />
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
      <div className="recentActivityContainer">
        <h3 className="recentActivityTitle">
          <div>
            <Activity style={{width: '1.5rem', height: '1.5rem', color: '#ffffff'}} />
          </div>
          Recent Activity
        </h3>
        <div className="space-y-3">
          {recentActivity.map((activity, idx) => (
            <div key={idx} className="activityItem">
              <div>
                <span className="activityTime">{activity.time}</span>
                <span className={`activityType ${
                  activity.type === 'Email' ? 'Email' :
                  activity.type === 'Facebook' ? 'Facebook' :
                  activity.type === 'Instagram' ? 'Instagram' :
                  'LinkedIn'
                }`}>
                  {activity.type}
                </span>
                <span className="activityDescription">{activity.details}</span>
              </div>
              <span className={`activityStatus ${
                activity.status === 'Success' ? 'success' : 'failure'
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
    <div style={{padding: '1rem'}}>
      {/* Header */}
      <div className="headerContainer">
        <div>
          <h2 className="headerTitle">Scheduled Posts</h2>
          <p className="headerSubtitle">Manage your social media content calendar</p>
        </div>
        <button
          onClick={() => setShowUploadModal(true)}
        >
          <Plus style={{width: '1.5rem', height: '1.5rem', color: '#ffffff'}} />
          New Post
        </button>
      </div>

      {/* Scheduled Posts List */}
      <div style={{padding: '1rem'}} >
        {scheduledPosts.map(post => (
          <div key={post.id} className="scheduledPostCard">
            <div style={{padding: '1rem', display: 'flex', justifyContent: 'space-between'}}>
              <div style={{display: 'flex', gap: '0.5rem', padding: '0.5rem'}}
>
                {/* Platform Icon */}
                <div className={`Icon ${post.platform}`} style={getPlatformColor(post.platform)}>
                  {getPlatformIcon(post.platform)}
                </div>

                {/* Post Details */}
                <div className="postDetails">
                  <div className="postHeader">
                    <h3>{post.platform}</h3>
                    <span className={`statusBadge ${
                      post.status === 'Pending' ? 'Pending' :
                      post.status === 'Posted' ? 'Posted' :
                      'Failed'
                    }`}>
                      {post.status}
                    </span>
                  </div>
                  <p className="postCaption">{post.caption}</p>
                  {post.hashtags && (
                    <p className="postHashtags">{post.hashtags}</p>
                  )}
                  <div className="postMeta">
                    <span>
                      <Calendar style={{width: '1rem', height: '1rem'}}/>
                      {post.date} at {post.time}
                    </span>
                    {post.media && (
                      <span>
                        <Upload style={{width:'1rem', height:'1rem'}}/>
                        {post.media}
                      </span>
                    )}
                  </div>
                </div>
              </div>

              {/* Actions */}
              <button
                onClick={() => handleDeletePost(post.id)}
                className="actionButton"
              >
                <X style={{width: '1.5rem', height: '1.5rem'}}/>
              </button>
            </div>
          </div>
        ))}
      </div>

      {scheduledPosts.length === 0 && (
        <div className="noScheduledPosts">
          <Upload style={{width: '5rem', height: '5rem', color: '#9ca3af', marginLeft: 'auto', marginRight: 'auto', marginBottom: '1rem'}} />
          <h3>No scheduled posts</h3>
          <p>Get started by scheduling your first post</p>
          <button
            onClick={() => setShowUploadModal(true)}
          >
            <Plus style={{width: '1.5rem', height: '1.5rem', marginLeft: 'auto', marginRight: 'auto'}} />
            Schedule Post
          </button>
        </div>
      )}
    </div>
  );

  return (
    <div className="appContainer">
      {/* Header */}
      <header>
        <div 
        className='headerContainer'>
          <div className="headerContent">
            <div className="headerLeft">
              <div className="IconWrapper">
                <Activity style={{color: 'white', width: '2rem', height: '2rem'}} />
              </div>
              <div className='titleGroup'>
                <h1>Sales Automation</h1>
                <p>Multi-Platform Campaign Manager</p>
              </div>
            </div>
            <div className="headerActions">
              <button className="iconButton">
                <RefreshCw style={{width:'2rem', height:'2rem'}}/>
              </button>
              <button className="iconButton">
                <Download style={{width:'2rem', height:'2rem'}}/>
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