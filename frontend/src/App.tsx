import React, { useState, useRef } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import html2canvas from 'html2canvas';
import jsPDF from 'jspdf';
import { 
  Upload, MessageSquare, Send, Loader2, Leaf, 
  Image as ImageIcon, CheckCircle2, Download, 
  FileText, ShieldCheck, Info
} from 'lucide-react';
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
  const reportRef = useRef<HTMLDivElement>(null);

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
      setError('请描述您观察到的症状');
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

      if (!response.ok) throw new Error('诊断服务响应异常');
      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : '连接服务失败');
    } finally {
      setLoading(false);
    }
  };

  const downloadMarkdown = () => {
    if (!result) return;
    const blob = new Blob([result.answer_markdown], { type: 'text/markdown' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `诊断报告_${result.detection.pest_type}.md`;
    link.click();
  };

  const downloadPDF = async () => {
    if (!reportRef.current) return;
    const canvas = await html2canvas(reportRef.current, { scale: 2 });
    const imgData = canvas.toDataURL('image/png');
    const pdf = new jsPDF('p', 'mm', 'a4');
    const imgProps = pdf.getImageProperties(imgData);
    const pdfWidth = pdf.internal.pageSize.getWidth();
    const pdfHeight = (imgProps.height * pdfWidth) / imgProps.width;
    pdf.addImage(imgData, 'PNG', 0, 0, pdfWidth, pdfHeight);
    pdf.save(`浆果诊断报告_${new Date().toLocaleDateString()}.pdf`);
  };

  return (
    <div className="dashboard">
      {/* LEFT SIDEBAR */}
      <aside className="sidebar">
        <div className="brand">
          <Leaf size={32} color="var(--primary-light)" fill="var(--primary-light)" />
          <h1>浆果智能诊断系统</h1>
        </div>

        <div className="input-section">
          <div className="input-group">
            <label className="field-label"><MessageSquare size={16} /> 症状详述</label>
            <textarea 
              className="text-area" 
              rows={6}
              placeholder="请详细描述病害部位、颜色、蔓延情况..."
              value={query}
              onChange={(e) => setQuery(e.target.value)}
            />
          </div>

          <div className="input-group">
            <label className="field-label"><ImageIcon size={16} /> 现场实拍</label>
            <div className="dropzone" onClick={() => fileInputRef.current?.click()}>
              <input type="file" hidden ref={fileInputRef} onChange={handleFileChange} accept="image/*" />
              {preview ? (
                <div className="preview-wrapper">
                  <img src={preview} alt="Preview" className="preview-img" />
                </div>
              ) : (
                <>
                  <Upload size={32} color="var(--text-muted)" style={{ marginBottom: '12px' }} />
                  <p style={{ fontSize: '0.9rem', fontWeight: 500 }}>点击或拖拽上传</p>
                  <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>支持高清 JPG/PNG</span>
                </>
              )}
            </div>
          </div>
        </div>

        {error && <p style={{ color: 'var(--accent)', fontSize: '0.85rem', marginBottom: '1rem' }}>{error}</p>}

        <button className="btn-submit" onClick={handleDiagnose} disabled={loading}>
          {loading ? <Loader2 className="spinner" /> : <Send size={20} />}
          {loading ? '正在深度分析...' : '开启智能诊断'}
        </button>
      </aside>

      {/* RIGHT STAGE */}
      <main className="content-stage">
        {!result && !loading && (
          <div className="welcome-screen">
            <ShieldCheck size={64} color="var(--border)" strokeWidth={1} />
            <h2 style={{ marginTop: '1.5rem', color: 'var(--text-main)' }}>准备好开启智慧诊断了吗？</h2>
            <p style={{ maxWidth: '400px', margin: '1rem auto' }}>上传浆果照片，我们将结合 YOLO 视觉模型与多模态 RAG 知识库为您提供专业建议。</p>
          </div>
        )}

        {loading && (
          <div className="welcome-screen">
            <div className="loading-pulse">
              <Loader2 size={64} className="spinner" color="var(--primary-light)" />
            </div>
            <h3 style={{ marginTop: '2rem' }}>系统正在接入 Gemini 3.0 Flash...</h3>
            <p>正在检索本地知识块并构建多模态 Prompt</p>
          </div>
        )}

        {result && (
          <div className="result-view">
            <div className="toolbar">
              <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                <CheckCircle2 color="var(--primary-light)" />
                <span style={{ fontWeight: 700, color: 'var(--primary)' }}>诊断已就绪</span>
              </div>
              <div className="export-btns">
                <button className="btn-export" onClick={downloadMarkdown}>
                  <FileText size={16} /> 导出 Markdown
                </button>
                <button className="btn-export" onClick={downloadPDF} style={{ background: 'var(--primary)', color: 'white', borderColor: 'var(--primary)' }}>
                  <Download size={16} /> 下载 PDF 报告
                </button>
              </div>
            </div>

            <div className="report-card" ref={reportRef}>
              <div className="status-badge">
                <ShieldCheck size={14} /> 模型认证诊断
              </div>
              
              <div className="markdown-content">
                <ReactMarkdown remarkPlugins={[remarkGfm]}>{result.answer_markdown}</ReactMarkdown>
              </div>

              <div className="knowledge-section">
                <h2 style={{ marginBottom: '1.5rem' }}>溯源依据</h2>
                <div className="knowledge-grid">
                  {result.retrieved.map((item) => (
                    <div key={item.id} className="knowledge-card">
                      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
                        <span className="score-tag">命中评分: {(item.score * 100).toFixed(0)}</span>
                        <Info size={14} color="var(--text-muted)" />
                      </div>
                      <h4>{item.title}</h4>
                      <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>{item.content}</p>
                    </div>
                  ))}
                </div>
              </div>

              <div style={{ marginTop: '4rem', padding: '1.5rem', borderTop: '1px solid var(--border)', display: 'flex', justifyContent: 'space-between', fontSize: '0.75rem', color: 'var(--text-muted)' }}>
                <span>视觉指纹: YOLOv8-{result.detection.pest_type} ({result.detection.confidence})</span>
                <span>生成引擎: Gemini-3.0-Flash (Multi-modal)</span>
                <span>报告编号: {Math.random().toString(36).substr(2, 9).toUpperCase()}</span>
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
