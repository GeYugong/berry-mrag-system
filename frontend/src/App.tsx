import React, { useState, useRef } from 'react';
import ReactMarkdown from 'react-markdown';
import { Upload, MessageSquare, Send, Loader2, Leaf, Image as ImageIcon, CheckCircle2 } from 'lucide-react';
import './App.css';

interface Detection {
  pest_type: string;
  confidence: number;
  bbox: number[];
}

interface RetrievalItem {
  id: string;
  title: string;
  content: string;
  score: number;
}

interface DiagnosisResult {
  detection: Detection;
  retrieved: RetrievalItem[];
  answer_markdown: string;
}

const API_BASE = 'http://localhost:8000/api';

function App() {
  const [query, setQuery] = useState('');
  const [file, setFile] = useState<File | null>(null);
  const [preview, setPreview] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<DiagnosisResult | null>(null);
  const [error, setError] = useState<string | null>(null);
  
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = e.target.files?.[0];
    if (selectedFile) {
      setFile(selectedFile);
      setPreview(URL.createObjectURL(selectedFile));
      setError(null);
    }
  };

  const handleDiagnose = async () => {
    if (!query.trim()) {
      setError('请输入您的问题');
      return;
    }

    setLoading(true);
    setError(null);
    
    const formData = new FormData();
    formData.append('query', query);
    if (file) {
      formData.append('file', file);
    }

    try {
      const response = await fetch(`${API_BASE}/diagnose/upload`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('诊断服务响应异常');
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : '连接服务失败，请检查后端是否启动');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-container">
      <header>
        <h1><Leaf style={{ verticalAlign: 'middle', marginRight: '8px' }} /> 浆果智能 MRAG 系统</h1>
        <p>基于感知-认知-生成的多模态病虫害决策支持平台</p>
      </header>

      <div className="main-grid">
        {/* Input Section */}
        <section className="input-card">
          <div className="input-group">
            <label><MessageSquare size={16} /> 描述您发现的问题</label>
            <textarea 
              className="text-input" 
              rows={4}
              placeholder="例如：草莓叶片上有白色粉末状物质，已经蔓延到果实了..."
              value={query}
              onChange={(e) => setQuery(e.target.value)}
            />
          </div>

          <div className="input-group">
            <label><ImageIcon size={16} /> 上传病灶图片 (可选)</label>
            <div 
              className="upload-zone"
              onClick={() => fileInputRef.current?.click()}
            >
              <input 
                type="file" 
                hidden 
                ref={fileInputRef} 
                onChange={handleFileChange}
                accept="image/*"
              />
              {preview ? (
                <div className="preview-container">
                  <img src={preview} alt="Preview" className="image-preview" />
                  <p style={{ marginTop: '8px', fontSize: '0.75rem', color: 'var(--primary-green)' }}>点击更换图片</p>
                </div>
              ) : (
                <>
                  <Upload size={32} style={{ color: 'var(--text-muted)', marginBottom: '8px' }} />
                  <p>点击或拖拽上传图片</p>
                  <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>支持 JPG, PNG 格式</span>
                </>
              )}
            </div>
          </div>

          {error && <p style={{ color: 'var(--primary-red)', marginBottom: '1rem', fontSize: '0.875rem' }}>{error}</p>}

          <button 
            className="btn-diagnose" 
            onClick={handleDiagnose}
            disabled={loading}
          >
            {loading ? <Loader2 className="spinner" /> : <Send size={18} />}
            {loading ? '诊断中...' : '开始智能诊断'}
          </button>
        </section>

        {/* Result Section */}
        <section className="result-card">
          {!result && !loading && (
            <div style={{ textAlign: 'center', padding: '4rem 0', color: 'var(--text-muted)' }}>
              <ImageIcon size={48} style={{ opacity: 0.2, marginBottom: '1rem' }} />
              <p>请在左侧输入信息并开始诊断</p>
            </div>
          )}

          {loading && (
            <div style={{ textAlign: 'center', padding: '4rem 0' }}>
              <Loader2 size={48} className="spinner" style={{ color: 'var(--primary-green)', marginBottom: '1rem' }} />
              <p>系统正在分析多模态数据...</p>
            </div>
          )}

          {result && (
            <div className="diagnosis-content">
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '1rem' }}>
                <CheckCircle2 color="var(--primary-green)" />
                <h3 style={{ margin: 0 }}>诊断报告已生成</h3>
              </div>

              <div className="markdown-body">
                <ReactMarkdown>{result.answer_markdown}</ReactMarkdown>
              </div>

              <div className="sources-list">
                <h3 style={{ fontSize: '1.125rem', color: 'var(--text-main)', borderLeft: '4px solid var(--primary-green)', paddingLeft: '12px' }}>
                  知识库召回依据
                </h3>
                {result.retrieved.map((item) => (
                  <div key={item.id} className="source-item">
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                      <h4>{item.title}</h4>
                      <span className="score">相关性: {(item.score * 100).toFixed(1)}%</span>
                    </div>
                    <p style={{ fontSize: '0.875rem', color: 'var(--text-muted)', marginTop: '4px' }}>{item.content}</p>
                  </div>
                ))}
              </div>
              
              <div style={{ marginTop: '2rem', padding: '1rem', background: '#f1f5f9', borderRadius: '0.5rem', fontSize: '0.75rem' }}>
                <strong>视觉模型技术参数:</strong> Model: YOLOv8n | Pest: {result.detection.pest_type} | Conf: {result.detection.confidence}
              </div>
            </div>
          )}
        </section>
      </div>
    </div>
  );
}

export default App;
