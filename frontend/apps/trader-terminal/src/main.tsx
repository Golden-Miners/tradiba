import React from 'react'
import ReactDOM from 'react-dom/client'
import { Workspace } from './components/workspace/Workspace'
import './index.css'

ReactDOM.createRoot(document.getElementById('root') as HTMLElement).render(
  <React.StrictMode>
    <Workspace />
  </React.StrictMode>,
)
