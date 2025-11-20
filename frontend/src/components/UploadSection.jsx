import { useState, useRef } from 'react'
import axios from 'axios'

function UploadSection({ setCurrentPresentation, setPresentationStructure, setLoading }) {
  const [content, setContent] = useState('')
  const [audienceType, setAudienceType] = useState('corporate')
  const [uploadedFiles, setUploadedFiles] = useState({})
  const [activeTab, setActiveTab] = useState('text')
  const fileInputRef = useRef(null)
  const templateInputRef = useRef(null)
  const dataInputRef = useRef(null)

  const handleFileUpload = async (file, type) => {
    const formData = new FormData()
    formData.append('file', file)

    try {
      const response = await axios.post('/api/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      })
      
      setUploadedFiles(prev => ({
        ...prev,
        [type]: response.data.filepath
      }))
      
      return response.data.filepath
    } catch (error) {
      alert('Error uploading file: ' + (error.response?.data?.error || error.message))
      return null
    }
  }

  const handleGenerate = async () => {
    if (!content && !uploadedFiles.reference) {
      alert('Please provide content or upload a reference presentation')
      return
    }

    setLoading(true)
    try {
      let response
      
      if (uploadedFiles.reference && content) {
        response = await axios.post('/api/style-transfer', {
          reference_path: uploadedFiles.reference,
          content: content,
          audience_type: audienceType
        })
      } else {
        response = await axios.post('/api/generate', {
          content: content,
          audience_type: audienceType,
          template_path: uploadedFiles.template
        })
      }

      setCurrentPresentation(response.data)
      setPresentationStructure(response.data.structure)
      alert('Presentation generated successfully!')
    } catch (error) {
      alert('Error generating presentation: ' + (error.response?.data?.error || error.message))
    } finally {
      setLoading(false)
    }
  }

  const handleGenerateChart = async () => {
    if (!uploadedFiles.data) {
      alert('Please upload a data file (CSV or Excel)')
      return
    }

    setLoading(true)
    try {
      const response = await axios.post('/api/chart', {
        data_filepath: uploadedFiles.data,
        chart_type: null,
        title: 'Data Visualization'
      })

      alert('Chart generated successfully! Path: ' + response.data.chart_info.chart_path)
    } catch (error) {
      alert('Error generating chart: ' + (error.response?.data?.error || error.message))
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h2 className="text-2xl font-bold text-gray-800 mb-4">Create Presentation</h2>

      <div className="flex space-x-2 mb-4 border-b border-gray-200">
        <button
          className={`px-4 py-2 font-medium ${
            activeTab === 'text'
              ? 'text-primary border-b-2 border-primary'
              : 'text-gray-500 hover:text-gray-700'
          }`}
          onClick={() => setActiveTab('text')}
        >
          Text Input
        </button>
        <button
          className={`px-4 py-2 font-medium ${
            activeTab === 'upload'
              ? 'text-primary border-b-2 border-primary'
              : 'text-gray-500 hover:text-gray-700'
          }`}
          onClick={() => setActiveTab('upload')}
        >
          Upload Files
        </button>
        <button
          className={`px-4 py-2 font-medium ${
            activeTab === 'chart'
              ? 'text-primary border-b-2 border-primary'
              : 'text-gray-500 hover:text-gray-700'
          }`}
          onClick={() => setActiveTab('chart')}
        >
          Generate Chart
        </button>
      </div>

      {activeTab === 'text' && (
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Content
            </label>
            <textarea
              className="w-full h-48 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent"
              placeholder="Enter your presentation content here... (e.g., research summary, meeting notes, report)"
              value={content}
              onChange={(e) => setContent(e.target.value)}
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Audience Type
            </label>
            <select
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent"
              value={audienceType}
              onChange={(e) => setAudienceType(e.target.value)}
            >
              <option value="corporate">Corporate</option>
              <option value="academic">Academic</option>
              <option value="creative">Creative</option>
              <option value="minimalist">Minimalist</option>
            </select>
          </div>

          <button
            className="w-full bg-primary hover:bg-blue-700 text-white font-bold py-3 px-4 rounded-md transition duration-200"
            onClick={handleGenerate}
          >
            Generate Presentation
          </button>
        </div>
      )}

      {activeTab === 'upload' && (
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Reference Presentation (for style transfer)
            </label>
            <input
              type="file"
              ref={fileInputRef}
              accept=".pptx,.potx"
              className="hidden"
              onChange={(e) => e.target.files[0] && handleFileUpload(e.target.files[0], 'reference')}
            />
            <button
              className="w-full bg-gray-100 hover:bg-gray-200 text-gray-700 font-medium py-2 px-4 rounded-md border border-gray-300 transition duration-200"
              onClick={() => fileInputRef.current?.click()}
            >
              {uploadedFiles.reference ? '✓ Reference Uploaded' : 'Upload Reference PPTX'}
            </button>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Template (optional)
            </label>
            <input
              type="file"
              ref={templateInputRef}
              accept=".pptx,.potx"
              className="hidden"
              onChange={(e) => e.target.files[0] && handleFileUpload(e.target.files[0], 'template')}
            />
            <button
              className="w-full bg-gray-100 hover:bg-gray-200 text-gray-700 font-medium py-2 px-4 rounded-md border border-gray-300 transition duration-200"
              onClick={() => templateInputRef.current?.click()}
            >
              {uploadedFiles.template ? '✓ Template Uploaded' : 'Upload Template'}
            </button>
          </div>

          {uploadedFiles.reference && (
            <div className="pt-4">
              <textarea
                className="w-full h-32 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent mb-4"
                placeholder="Enter new content to apply the reference style to..."
                value={content}
                onChange={(e) => setContent(e.target.value)}
              />
              <button
                className="w-full bg-secondary hover:bg-blue-600 text-white font-bold py-3 px-4 rounded-md transition duration-200"
                onClick={handleGenerate}
              >
                Apply Style Transfer
              </button>
            </div>
          )}
        </div>
      )}

      {activeTab === 'chart' && (
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Data File (CSV or Excel)
            </label>
            <input
              type="file"
              ref={dataInputRef}
              accept=".csv,.xlsx,.xls"
              className="hidden"
              onChange={(e) => e.target.files[0] && handleFileUpload(e.target.files[0], 'data')}
            />
            <button
              className="w-full bg-gray-100 hover:bg-gray-200 text-gray-700 font-medium py-2 px-4 rounded-md border border-gray-300 transition duration-200"
              onClick={() => dataInputRef.current?.click()}
            >
              {uploadedFiles.data ? '✓ Data File Uploaded' : 'Upload Data File'}
            </button>
          </div>

          {uploadedFiles.data && (
            <button
              className="w-full bg-accent hover:bg-blue-500 text-white font-bold py-3 px-4 rounded-md transition duration-200"
              onClick={handleGenerateChart}
            >
              Generate Chart
            </button>
          )}

          <div className="bg-blue-50 border border-blue-200 rounded-md p-4 mt-4">
            <p className="text-sm text-gray-700">
              <strong>Tip:</strong> Upload a CSV or Excel file with your data. The system will automatically 
              infer the best chart type and generate a caption using AI.
            </p>
          </div>
        </div>
      )}
    </div>
  )
}

export default UploadSection
