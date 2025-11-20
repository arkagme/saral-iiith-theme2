function PreviewSection({ presentation, structure }) {
  if (!presentation) return null

  const handleDownload = () => {
    const link = document.createElement('a')
    link.href = `/api/download/${presentation.filename}`
    link.download = presentation.filename
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
  }

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h2 className="text-2xl font-bold text-gray-800 mb-4">Preview & Download</h2>

      {presentation.evaluation && (
        <div className="mb-6 p-4 bg-gradient-to-r from-blue-50 to-indigo-50 rounded-lg border border-blue-200">
          <h3 className="font-semibold text-gray-800 mb-2">Quality Evaluation</h3>
          <div className="grid grid-cols-2 gap-4 text-sm">
            <div>
              <p className="text-gray-600">Overall Score</p>
              <p className="text-2xl font-bold text-primary">
                {presentation.evaluation.overall_score.toFixed(1)}%
              </p>
            </div>
            <div>
              <p className="text-gray-600">Content F1 Score</p>
              <p className="text-2xl font-bold text-secondary">
                {(presentation.evaluation.content_consistency.keyword_f1_score * 100).toFixed(1)}%
              </p>
            </div>
          </div>
          <p className="mt-3 text-sm text-gray-700">
            {presentation.evaluation.recommendation}
          </p>
        </div>
      )}


      {structure && structure.slides && (
        <div className="mb-6">
          <h3 className="font-semibold text-gray-800 mb-3">Slide Structure</h3>
          <div className="space-y-2 max-h-64 overflow-y-auto">
            {structure.slides.map((slide, index) => (
              <div
                key={index}
                className="p-3 bg-gray-50 rounded-md border border-gray-200 hover:border-primary transition-colors"
              >
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <span className="text-xs font-medium text-gray-500">
                      Slide {index + 1} • {slide.type}
                    </span>
                    <p className="font-medium text-gray-800 mt-1">
                      {slide.title || slide.subtitle || 'Untitled'}
                    </p>
                    {slide.content && (
                      <p className="text-xs text-gray-600 mt-1">
                        {slide.content.length} bullet points
                      </p>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}


      {presentation.visual_style && (
        <div className="mb-6 p-4 bg-gray-50 rounded-lg">
          <h3 className="font-semibold text-gray-800 mb-2">Visual Style</h3>
          <div className="grid grid-cols-2 gap-2 text-sm">
            <div>
              <p className="text-gray-600">Tone</p>
              <p className="font-medium text-gray-800">{presentation.visual_style.tone}</p>
            </div>
            <div>
              <p className="text-gray-600">Font</p>
              <p className="font-medium text-gray-800">{presentation.visual_style.font_suggestion}</p>
            </div>
          </div>
          <div className="mt-3">
            <p className="text-gray-600 text-sm mb-2">Color Palette</p>
            <div className="flex space-x-2">
              {presentation.visual_style.primary_color && (
                <div
                  className="w-12 h-12 rounded border border-gray-300"
                  style={{ backgroundColor: presentation.visual_style.primary_color }}
                  title="Primary"
                />
              )}
              {presentation.visual_style.secondary_color && (
                <div
                  className="w-12 h-12 rounded border border-gray-300"
                  style={{ backgroundColor: presentation.visual_style.secondary_color }}
                  title="Secondary"
                />
              )}
              {presentation.visual_style.accent_color && (
                <div
                  className="w-12 h-12 rounded border border-gray-300"
                  style={{ backgroundColor: presentation.visual_style.accent_color }}
                  title="Accent"
                />
              )}
            </div>
          </div>
        </div>
      )}


      <button
        className="w-full bg-green-600 hover:bg-green-700 text-white font-bold py-3 px-4 rounded-md transition duration-200 flex items-center justify-center"
        onClick={handleDownload}
      >
        <svg
          className="w-5 h-5 mr-2"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"
          />
        </svg>
        Download Presentation
      </button>
    </div>
  )
}

export default PreviewSection
