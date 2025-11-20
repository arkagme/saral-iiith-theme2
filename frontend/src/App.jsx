import { useState } from 'react'
import UploadSection from './components/UploadSection'
import ChatInterface from './components/ChatInterface'
import PreviewSection from './components/PreviewSection'

function App() {
  const [currentPresentation, setCurrentPresentation] = useState(null)
  const [presentationStructure, setPresentationStructure] = useState(null)
  const [loading, setLoading] = useState(false)

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50">

      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <h1 className="text-3xl font-bold text-gray-900">
            AI PowerPoint Customization Engine
          </h1>
          <p className="mt-2 text-sm text-gray-600">
            Generate and customize professional presentations using AI
          </p>
        </div>
      </header>


      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">

          <div className="space-y-6">
            <UploadSection
              setCurrentPresentation={setCurrentPresentation}
              setPresentationStructure={setPresentationStructure}
              setLoading={setLoading}
            />
            
            {currentPresentation && (
              <PreviewSection
                presentation={currentPresentation}
                structure={presentationStructure}
              />
            )}
          </div>


          <div className="lg:sticky lg:top-8 lg:self-start">
            <ChatInterface
              currentPresentation={currentPresentation}
              presentationStructure={presentationStructure}
              setCurrentPresentation={setCurrentPresentation}
              setPresentationStructure={setPresentationStructure}
              setLoading={setLoading}
            />
          </div>
        </div>


        {loading && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
            <div className="bg-white rounded-lg p-8 max-w-sm w-full mx-4">
              <div className="flex flex-col items-center">
                <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-primary"></div>
                <p className="mt-4 text-gray-700 font-medium">Processing...</p>
              </div>
            </div>
          </div>
        )}
      </main>


      <footer className="bg-white border-t border-gray-200 mt-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <p className="text-center text-sm text-gray-500">
            AI-Powered PowerPoint Customization Engine - Built with Gemini 2.0 Flash Lite
          </p>
        </div>
      </footer>
    </div>
  )
}

export default App
