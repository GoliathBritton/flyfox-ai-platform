#!/usr/bin/env python3
"""
FLYFOX AI Web Application Integration Script
Automates the integration of modern web app structure into FLYFOX AI platform
"""

import os
import json
import shutil
from pathlib import Path
from typing import Dict, List, Any

class FlyfoxWebAppIntegrator:
    def __init__(self):
        self.project_name = "flyfox-ai-platform"
        self.branding = {
            "name": "FLYFOX AI",
            "company": "Goliath of All Trade Inc.",
            "contact": "john.britton@goliathomniedge.com",
            "mission": "SOLVE PROBLEMS & PROVIDE DYNAMIC AI SOLUTIONS",
            "colors": {
                "primary": "#FF6B35",
                "secondary": "#2C3E50", 
                "accent": "#E74C3C"
            }
        }
        
    def create_project_structure(self) -> Path:
        """Create the FLYFOX AI platform project structure"""
        print("🚀 Creating FLYFOX AI Platform Project Structure...")
        
        # Create project directory
        project_dir = Path(self.project_name)
        project_dir.mkdir(exist_ok=True)
        
        # Create directory structure
        directories = [
            "src/components",
            "src/pages", 
            "src/lib",
            "src/constants",
            "src/components/auth",
            "src/components/services",
            "public/partners",
            "public/images"
        ]
        
        for directory in directories:
            (project_dir / directory).mkdir(parents=True, exist_ok=True)
            
        print(f"✅ Project structure created at: {project_dir.absolute()}")
        return project_dir
        
    def create_package_json(self, project_dir: Path):
        """Create package.json with FLYFOX AI dependencies"""
        print("📦 Creating package.json...")
        
        package_json = {
            "name": "flyfox-ai-platform",
            "private": True,
            "version": "0.0.0",
            "type": "module",
            "scripts": {
                "dev": "vite",
                "build": "tsc && vite build",
                "lint": "eslint . --ext ts,tsx --report-unused-disable-directives --max-warnings 0",
                "preview": "vite preview"
            },
            "dependencies": {
                "react": "^18.2.0",
                "react-dom": "^18.2.0",
                "@supabase/supabase-js": "^2.39.0",
                "@supabase/ssr": "^0.0.10",
                "lucide-react": "^0.294.0"
            },
            "devDependencies": {
                "@types/react": "^18.2.43",
                "@types/react-dom": "^18.2.17",
                "@typescript-eslint/eslint-plugin": "^6.14.0",
                "@typescript-eslint/parser": "^6.14.0",
                "@vitejs/plugin-react": "^4.2.1",
                "autoprefixer": "^10.4.16",
                "eslint": "^8.55.0",
                "eslint-plugin-react-hooks": "^4.6.0",
                "eslint-plugin-react-refresh": "^0.4.5",
                "postcss": "^8.4.32",
                "tailwindcss": "^3.3.6",
                "typescript": "^5.2.2",
                "vite": "^5.0.8"
            }
        }
        
        with open(project_dir / "package.json", "w") as f:
            json.dump(package_json, f, indent=2)
            
        print("✅ package.json created")
        
    def create_tailwind_config(self, project_dir: Path):
        """Create Tailwind CSS configuration with FLYFOX AI colors"""
        print("🎨 Creating Tailwind CSS configuration...")
        
        tailwind_config = '''import type { Config } from 'tailwindcss'

export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'flyfox': {
          primary: '#FF6B35',
          secondary: '#2C3E50',
          accent: '#E74C3C',
        }
      },
      fontFamily: {
        'inter': ['Inter', 'sans-serif'],
      }
    },
  },
  plugins: [],
} satisfies Config
'''
        
        with open(project_dir / "tailwind.config.ts", "w") as f:
            f.write(tailwind_config)
            
        print("✅ Tailwind CSS configuration created")
        
    def create_branding_constants(self, project_dir: Path):
        """Create FLYFOX AI branding constants"""
        print("🏢 Creating FLYFOX AI branding constants...")
        
        branding_ts = f'''// src/constants/branding.ts
export const FLYFOX_AI_BRANDING = {{
  name: "{self.branding['name']}",
  company: "{self.branding['company']}",
  contact: "{self.branding['contact']}",
  mission: "{self.branding['mission']}",
  colors: {{
    primary: "{self.branding['colors']['primary']}",
    secondary: "{self.branding['colors']['secondary']}",
    accent: "{self.branding['colors']['accent']}",
    gradient: "linear-gradient(135deg, {self.branding['colors']['primary']} 0%, {self.branding['colors']['accent']} 100%)"
  }}
}}

export const FLYFOX_AI_SERVICES = {{
  quantumVoice: "{self.branding['name']} Quantum Voice Calling",
  videoCreation: "{self.branding['name']} Video Creation", 
  digitalAvatars: "{self.branding['name']} Digital Avatars",
  enterpriseAutomation: "{self.branding['name']} Enterprise Automation",
  whiteLabelSaaS: "{self.branding['name']} White-Label SaaS",
  consulting: "{self.branding['name']} Consulting"
}}

export const TECHNOLOGY_PARTNERS = {{
  openai: {{
    name: "OpenAI",
    description: "Advanced AI Language Models & API Integration",
    logo: "/partners/openai-logo.png"
  }},
  nvidia: {{
    name: "NVIDIA", 
    description: "Digital Avatars & GPU Acceleration Technology",
    logo: "/partners/nvidia-logo.png"
  }},
  dynex: {{
    name: "Dynex",
    description: "Quantum Computing & Neuromorphic Processing", 
    logo: "/partners/dynex-logo.png"
  }},
  twilio: {{
    name: "Twilio",
    description: "Voice Communication Infrastructure",
    logo: "/partners/twilio-logo.png"
  }}
}}
'''
        
        with open(project_dir / "src/constants/branding.ts", "w") as f:
            f.write(branding_ts)
            
        print("✅ FLYFOX AI branding constants created")
        
    def create_header_component(self, project_dir: Path):
        """Create Header component with FLYFOX AI branding"""
        print("📋 Creating Header component...")
        
        header_tsx = '''// src/components/Header.tsx
import { FLYFOX_AI_BRANDING } from '../constants/branding'

export function Header() {
  return (
    <header className="bg-white border-b border-gray-200 shadow-sm">
      <div className="container mx-auto px-6 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <div className="w-8 h-8 bg-gradient-to-r from-flyfox-primary to-flyfox-accent rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-sm">F</span>
            </div>
            <span className="text-xl font-bold text-gray-900">
              {FLYFOX_AI_BRANDING.name}
            </span>
          </div>
          <nav className="flex items-center space-x-6">
            <a href="#solutions" className="text-gray-700 hover:text-flyfox-primary transition-colors">
              Solutions
            </a>
            <a href="#technology" className="text-gray-700 hover:text-flyfox-primary transition-colors">
              Technology
            </a>
            <a href="/partners" className="text-gray-700 hover:text-flyfox-primary transition-colors">
              Partners
            </a>
            <a href="#contact" className="text-gray-700 hover:text-flyfox-primary transition-colors">
              Contact
            </a>
          </nav>
        </div>
      </div>
    </header>
  )
}
'''
        
        with open(project_dir / "src/components/Header.tsx", "w") as f:
            f.write(header_tsx)
            
        print("✅ Header component created")
        
    def create_footer_component(self, project_dir: Path):
        """Create Footer component with FLYFOX AI branding"""
        print("📋 Creating Footer component...")
        
        footer_tsx = f'''// src/components/Footer.tsx
import {{ FLYFOX_AI_BRANDING }} from '../constants/branding'

export function Footer() {{
  return (
    <footer className="bg-gray-900 text-white">
      <div className="container mx-auto px-6 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          <div>
            <h3 className="text-xl font-bold mb-4">{{FLYFOX_AI_BRANDING.name}}</h3>
            <p className="text-gray-300 mb-2">by {{FLYFOX_AI_BRANDING.company}}</p>
            <p className="text-gray-300 mb-4">{{FLYFOX_AI_BRANDING.mission}}</p>
            <p className="text-gray-300">Contact: {{FLYFOX_AI_BRANDING.contact}}</p>
          </div>
          <div>
            <h4 className="font-semibold mb-4">Solutions</h4>
            <ul className="space-y-2">
              <li><a href="#" className="text-gray-300 hover:text-white">Quantum Voice Calling</a></li>
              <li><a href="#" className="text-gray-300 hover:text-white">AI Video Creation</a></li>
              <li><a href="#" className="text-gray-300 hover:text-white">Digital Avatars</a></li>
              <li><a href="#" className="text-gray-300 hover:text-white">Enterprise Automation</a></li>
            </ul>
          </div>
          <div>
            <h4 className="font-semibold mb-4">Technology</h4>
            <ul className="space-y-2">
              <li><a href="#" className="text-gray-300 hover:text-white">Quantum AI</a></li>
              <li><a href="#" className="text-gray-300 hover:text-white">Machine Learning</a></li>
              <li><a href="#" className="text-gray-300 hover:text-white">Voice Processing</a></li>
              <li><a href="#" className="text-gray-300 hover:text-white">Video Generation</a></li>
            </ul>
          </div>
          <div>
            <h4 className="font-semibold mb-4">Partners</h4>
            <ul className="space-y-2">
              <li><a href="/partners" className="text-gray-300 hover:text-white">Technology Partners</a></li>
              <li><a href="/partners" className="text-gray-300 hover:text-white">Enterprise Partners</a></li>
              <li><a href="/partners" className="text-gray-300 hover:text-white">Infrastructure Partners</a></li>
            </ul>
          </div>
        </div>
        <div className="border-t border-gray-800 mt-8 pt-8 text-center">
          <p className="text-gray-300">
            © 2024 {{FLYFOX_AI_BRANDING.name}} by {{FLYFOX_AI_BRANDING.company}}. All rights reserved.
          </p>
        </div>
      </div>
    </footer>
  )
}}
'''
        
        with open(project_dir / "src/components/Footer.tsx", "w") as f:
            f.write(footer_tsx)
            
        print("✅ Footer component created")
        
    def create_layout_component(self, project_dir: Path):
        """Create Layout component"""
        print("📋 Creating Layout component...")
        
        layout_tsx = '''// src/components/Layout.tsx
import { Header } from './Header'
import { Footer } from './Footer'

interface LayoutProps {
  children: React.ReactNode
}

export function Layout({ children }: LayoutProps) {
  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      <main className="flex-1">
        {children}
      </main>
      <Footer />
    </div>
  )
}
'''
        
        with open(project_dir / "src/components/Layout.tsx", "w") as f:
            f.write(layout_tsx)
            
        print("✅ Layout component created")
        
    def create_quantum_voice_component(self, project_dir: Path):
        """Create Quantum Voice Calling component"""
        print("📋 Creating Quantum Voice Calling component...")
        
        quantum_voice_tsx = '''// src/components/services/QuantumVoiceCalling.tsx
import { useState } from 'react'

export function QuantumVoiceCalling() {
  const [isCallActive, setIsCallActive] = useState(false)
  const [callDuration, setCallDuration] = useState(0)

  const startCall = () => {
    setIsCallActive(true)
    // Integration with FLYFOX AI quantum voice system
  }

  const endCall = () => {
    setIsCallActive(false)
    setCallDuration(0)
  }

  return (
    <div className="bg-white p-6 rounded-lg shadow-md">
      <h3 className="text-xl font-semibold text-gray-900 mb-4">
        FLYFOX AI Quantum Voice Calling
      </h3>
      <p className="text-gray-600 mb-6">
        Revolutionary voice calling powered by quantum computing and OpenAI technology.
      </p>
      
      <div className="space-y-4">
        <div className="flex items-center space-x-4">
          <button
            onClick={startCall}
            disabled={isCallActive}
            className="bg-flyfox-primary text-white px-4 py-2 rounded-lg hover:bg-flyfox-accent disabled:opacity-50"
          >
            Start Quantum Call
          </button>
          <button
            onClick={endCall}
            disabled={!isCallActive}
            className="bg-red-600 text-white px-4 py-2 rounded-lg hover:bg-red-700 disabled:opacity-50"
          >
            End Call
          </button>
        </div>
        
        {isCallActive && (
          <div className="bg-green-100 p-4 rounded-lg">
            <p className="text-green-800">
              Quantum call active - Duration: {callDuration}s
            </p>
          </div>
        )}
      </div>
      
      <div className="mt-4">
        <small className="text-gray-500">
          Technology powered by OpenAI, Dynex, and NVIDIA
        </small>
      </div>
    </div>
  )
}
'''
        
        with open(project_dir / "src/components/services/QuantumVoiceCalling.tsx", "w") as f:
            f.write(quantum_voice_tsx)
            
        print("✅ Quantum Voice Calling component created")
        
    def create_video_creation_component(self, project_dir: Path):
        """Create Video Creation component"""
        print("📋 Creating Video Creation component...")
        
        video_creation_tsx = '''// src/components/services/VideoCreation.tsx
import { useState } from 'react'

export function VideoCreation() {
  const [selectedTemplate, setSelectedTemplate] = useState('')
  const [selectedAvatar, setSelectedAvatar] = useState('')
  const [isGenerating, setIsGenerating] = useState(false)

  const generateVideo = async () => {
    setIsGenerating(true)
    // Integration with FLYFOX AI video creation system
    setTimeout(() => setIsGenerating(false), 3000)
  }

  return (
    <div className="bg-white p-6 rounded-lg shadow-md">
      <h3 className="text-xl font-semibold text-gray-900 mb-4">
        FLYFOX AI Video Creation
      </h3>
      <p className="text-gray-600 mb-6">
        Create professional videos with AI-powered avatars and quantum-enhanced scripting.
      </p>
      
      <div className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Select Template
          </label>
          <select
            value={selectedTemplate}
            onChange={(e) => setSelectedTemplate(e.target.value)}
            className="w-full border border-gray-300 rounded-lg px-3 py-2"
          >
            <option value="">Choose a template</option>
            <option value="presentation">Business Presentation</option>
            <option value="training">Training Video</option>
            <option value="marketing">Marketing Content</option>
          </select>
        </div>
        
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Select Avatar
          </label>
          <select
            value={selectedAvatar}
            onChange={(e) => setSelectedAvatar(e.target.value)}
            className="w-full border border-gray-300 rounded-lg px-3 py-2"
          >
            <option value="">Choose an avatar</option>
            <option value="professional">Professional</option>
            <option value="casual">Casual</option>
            <option value="creative">Creative</option>
          </select>
        </div>
        
        <button
          onClick={generateVideo}
          disabled={!selectedTemplate || !selectedAvatar || isGenerating}
          className="w-full bg-flyfox-primary text-white px-4 py-2 rounded-lg hover:bg-flyfox-accent disabled:opacity-50"
        >
          {isGenerating ? 'Generating Video...' : 'Generate Video'}
        </button>
      </div>
    </div>
  )
}
'''
        
        with open(project_dir / "src/components/services/VideoCreation.tsx", "w") as f:
            f.write(video_creation_tsx)
            
        print("✅ Video Creation component created")
        
    def create_partners_page(self, project_dir: Path):
        """Create Partners page"""
        print("📋 Creating Partners page...")
        
        partners_tsx = '''// src/pages/Partners.tsx
import { Layout } from '../components/Layout'

const partners = [
  {
    name: "OpenAI",
    description: "Advanced AI Language Models & API Integration",
    logo: "/partners/openai-logo.png",
    category: "Technology"
  },
  {
    name: "NVIDIA",
    description: "Digital Avatars & GPU Acceleration Technology",
    logo: "/partners/nvidia-logo.png",
    category: "Technology"
  },
  {
    name: "Dynex",
    description: "Quantum Computing & Neuromorphic Processing",
    logo: "/partners/dynex-logo.png",
    category: "Technology"
  },
  {
    name: "UiPath",
    description: "Robotic Process Automation Integration",
    logo: "/partners/uipath-logo.png",
    category: "Enterprise"
  },
  {
    name: "Prismatic",
    description: "Integration Platform as a Service",
    logo: "/partners/prismatic-logo.png",
    category: "Enterprise"
  }
]

export function PartnersPage() {
  return (
    <Layout>
      <div className="min-h-screen bg-gray-50">
        <div className="container mx-auto px-6 py-12">
          <div className="text-center mb-12">
            <h1 className="text-4xl font-bold text-gray-900 mb-4">
              Our Technology Partners
            </h1>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              FLYFOX AI collaborates with industry leaders to deliver cutting-edge quantum AI solutions.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {partners.map((partner) => (
              <div key={partner.name} className="bg-white p-6 rounded-lg shadow-md">
                <img 
                  src={partner.logo} 
                  alt={partner.name} 
                  className="h-12 mb-4"
                />
                <h3 className="text-xl font-semibold mb-2">{partner.name}</h3>
                <p className="text-gray-600">{partner.description}</p>
                <span className="inline-block mt-2 text-sm text-flyfox-primary font-medium">
                  {partner.category}
                </span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </Layout>
  )
}
'''
        
        with open(project_dir / "src/pages/Partners.tsx", "w") as f:
            f.write(partners_tsx)
            
        print("✅ Partners page created")
        
    def create_main_app(self, project_dir: Path):
        """Create main App component"""
        print("📋 Creating main App component...")
        
        app_tsx = '''// src/App.tsx
import { Layout } from './components/Layout'
import { QuantumVoiceCalling } from './components/services/QuantumVoiceCalling'
import { VideoCreation } from './components/services/VideoCreation'

function App() {
  return (
    <Layout>
      <div className="min-h-screen bg-gray-50">
        <div className="container mx-auto px-6 py-12">
          <div className="text-center mb-12">
            <h1 className="text-4xl font-bold text-gray-900 mb-4">
              FLYFOX AI Platform
            </h1>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Revolutionary quantum AI solutions for modern businesses
            </p>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            <QuantumVoiceCalling />
            <VideoCreation />
          </div>
        </div>
      </div>
    </Layout>
  )
}

export default App
'''
        
        with open(project_dir / "src/App.tsx", "w") as f:
            f.write(app_tsx)
            
        print("✅ Main App component created")
        
    def create_index_html(self, project_dir: Path):
        """Create index.html with FLYFOX AI branding"""
        print("📋 Creating index.html...")
        
        index_html = f'''<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" type="image/svg+xml" href="/vite.svg" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{self.branding['name']} - Quantum AI Solutions</title>
    <meta name="description" content="{self.branding['name']} by {self.branding['company']} - {self.branding['mission']}" />
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>
'''
        
        with open(project_dir / "index.html", "w") as f:
            f.write(index_html)
            
        print("✅ index.html created")
        
    def create_main_tsx(self, project_dir: Path):
        """Create main.tsx entry point"""
        print("📋 Creating main.tsx...")
        
        main_tsx = '''import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.tsx'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
'''
        
        with open(project_dir / "src/main.tsx", "w") as f:
            f.write(main_tsx)
            
        print("✅ main.tsx created")
        
    def create_index_css(self, project_dir: Path):
        """Create index.css with Tailwind imports"""
        print("📋 Creating index.css...")
        
        index_css = '''@tailwind base;
@tailwind components;
@tailwind utilities;

body {
  font-family: 'Inter', sans-serif;
}
'''
        
        with open(project_dir / "src/index.css", "w") as f:
            f.write(index_css)
            
        print("✅ index.css created")
        
    def create_vite_config(self, project_dir: Path):
        """Create Vite configuration"""
        print("📋 Creating Vite configuration...")
        
        vite_config = '''import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
})
'''
        
        with open(project_dir / "vite.config.ts", "w") as f:
            f.write(vite_config)
            
        print("✅ Vite configuration created")
        
    def create_tsconfig(self, project_dir: Path):
        """Create TypeScript configuration"""
        print("📋 Creating TypeScript configuration...")
        
        tsconfig = {
            "compilerOptions": {
                "target": "ES2020",
                "useDefineForClassFields": True,
                "lib": ["ES2020", "DOM", "DOM.Iterable"],
                "module": "ESNext",
                "skipLibCheck": True,
                "moduleResolution": "bundler",
                "allowImportingTsExtensions": True,
                "resolveJsonModule": True,
                "isolatedModules": True,
                "noEmit": True,
                "jsx": "react-jsx",
                "strict": True,
                "noUnusedLocals": True,
                "noUnusedParameters": True,
                "noFallthroughCasesInSwitch": True
            },
            "include": ["src"],
            "references": [{"path": "./tsconfig.node.json"}]
        }
        
        with open(project_dir / "tsconfig.json", "w") as f:
            json.dump(tsconfig, f, indent=2)
            
        print("✅ TypeScript configuration created")
        
    def create_readme(self, project_dir: Path):
        """Create README with FLYFOX AI branding"""
        print("📋 Creating README...")
        
        readme = f'''# {self.branding['name']} Platform

Modern web application for {self.branding['name']} by {self.branding['company']}.

## Mission
{self.branding['mission']}

## Contact
{self.branding['contact']}

## Technology Stack
- React 18
- TypeScript
- Vite
- Tailwind CSS
- Supabase (Authentication)
- Lucide React (Icons)

## Development

### Install Dependencies
```bash
npm install
```

### Start Development Server
```bash
npm run dev
```

### Build for Production
```bash
npm run build
```

### Preview Production Build
```bash
npm run preview
```

## Features
- FLYFOX AI Quantum Voice Calling
- FLYFOX AI Video Creation
- FLYFOX AI Digital Avatars
- FLYFOX AI Enterprise Automation
- Technology Partners Integration

## Branding
- Primary Brand: {self.branding['name']}
- Company: {self.branding['company']}
- Contact: {self.branding['contact']}
- Mission: {self.branding['mission']}

© 2024 {self.branding['name']} by {self.branding['company']}. All rights reserved.
'''
        
        with open(project_dir / "README.md", "w") as f:
            f.write(readme)
            
        print("✅ README created")
        
    def create_env_template(self, project_dir: Path):
        """Create environment variables template"""
        print("📋 Creating environment template...")
        
        env_template = '''# Environment Variables
# Copy this file to .env.local and fill in your values

VITE_SUPABASE_URL=your-supabase-url
VITE_SUPABASE_ANON_KEY=your-supabase-anon-key
VITE_FLYFOX_AI_API_URL=your-api-url
'''
        
        with open(project_dir / ".env.example", "w") as f:
            f.write(env_template)
            
        print("✅ Environment template created")
        
    def run_integration(self):
        """Run the complete integration process"""
        print("🚀 Starting FLYFOX AI Web Application Integration...")
        print("=" * 60)
        
        # Create project structure
        project_dir = self.create_project_structure()
        
        # Create configuration files
        self.create_package_json(project_dir)
        self.create_tailwind_config(project_dir)
        self.create_vite_config(project_dir)
        self.create_tsconfig(project_dir)
        
        # Create branding and constants
        self.create_branding_constants(project_dir)
        
        # Create components
        self.create_header_component(project_dir)
        self.create_footer_component(project_dir)
        self.create_layout_component(project_dir)
        self.create_quantum_voice_component(project_dir)
        self.create_video_creation_component(project_dir)
        
        # Create pages
        self.create_partners_page(project_dir)
        
        # Create main app files
        self.create_main_app(project_dir)
        self.create_index_html(project_dir)
        self.create_main_tsx(project_dir)
        self.create_index_css(project_dir)
        
        # Create documentation
        self.create_readme(project_dir)
        self.create_env_template(project_dir)
        
        print("=" * 60)
        print("🎉 FLYFOX AI Web Application Integration Complete!")
        print(f"📁 Platform created at: {project_dir.absolute()}")
        print("\n🚀 Next Steps:")
        print("1. cd flyfox-ai-platform")
        print("2. npm install")
        print("3. npm run dev")
        print("4. Open http://localhost:5173")
        print("\n📧 Contact: john.britton@goliathomniedge.com")
        
        return project_dir

def main():
    """Main function to run the integration"""
    integrator = FlyfoxWebAppIntegrator()
    integrator.run_integration()

if __name__ == "__main__":
    main() 