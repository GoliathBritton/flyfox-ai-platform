import { FLYFOX_AI_BRANDING } from './constants/branding'

function App() {
  return (
    <div className="min-h-screen bg-gray-50">
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
              <a href="#solutions" className="text-gray-700 hover:text-flyfox-primary">Solutions</a>
              <a href="#technology" className="text-gray-700 hover:text-flyfox-primary">Technology</a>
              <a href="/partners" className="text-gray-700 hover:text-flyfox-primary">Partners</a>
              <a href="#contact" className="text-gray-700 hover:text-flyfox-primary">Contact</a>
            </nav>
          </div>
        </div>
      </header>

      <main className="container mx-auto px-6 py-12">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            {FLYFOX_AI_BRANDING.name} Platform
          </h1>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Revolutionary quantum AI solutions for modern businesses
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <div className="bg-white p-6 rounded-lg shadow-md">
            <h3 className="text-xl font-semibold text-gray-900 mb-4">
              {FLYFOX_AI_BRANDING.name} Quantum Voice Calling
            </h3>
            <p className="text-gray-600 mb-6">
              Revolutionary voice calling powered by quantum computing and OpenAI technology.
            </p>
            <button className="bg-flyfox-primary text-white px-4 py-2 rounded-lg hover:bg-flyfox-accent">
              Start Quantum Call
            </button>
          </div>

          <div className="bg-white p-6 rounded-lg shadow-md">
            <h3 className="text-xl font-semibold text-gray-900 mb-4">
              {FLYFOX_AI_BRANDING.name} Video Creation
            </h3>
            <p className="text-gray-600 mb-6">
              Create professional videos with AI-powered avatars and quantum-enhanced scripting.
            </p>
            <button className="bg-flyfox-primary text-white px-4 py-2 rounded-lg hover:bg-flyfox-accent">
              Generate Video
            </button>
          </div>
        </div>
      </main>

      <footer className="bg-gray-900 text-white mt-12">
        <div className="container mx-auto px-6 py-12">
          <div className="text-center">
            <h3 className="text-xl font-bold mb-4">{FLYFOX_AI_BRANDING.name}</h3>
            <p className="text-gray-300 mb-2">by {FLYFOX_AI_BRANDING.company}</p>
            <p className="text-gray-300 mb-4">{FLYFOX_AI_BRANDING.mission}</p>
            <p className="text-gray-300">Contact: {FLYFOX_AI_BRANDING.contact}</p>
          </div>
        </div>
      </footer>
    </div>
  )
}

export default App
