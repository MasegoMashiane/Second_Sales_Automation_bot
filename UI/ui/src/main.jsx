import React from "react";
import reactDom from "react-dom/client";
import AutomationDashboard from "./AutomationDashboard";
import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'


createRoot(document.getElementById('root')).render(
  <StrictMode>
    <AutomationDashboard/>
  </StrictMode>,
)
