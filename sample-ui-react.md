```jsx
import React, { useState } from 'react';
import { 
  LayoutDashboard, 
  Database, 
  Cpu, 
  Activity, 
  Save, 
  Play, 
  Square, 
  Settings,
  Image as ImageIcon,
  FileText,
  BarChart2
} from 'lucide-react';

// --- Komponen-komponen UI Sederhana (Wireframe Style) ---

const Card = ({ title, children, className = "" }) => (
  <div className={`bg-white border-2 border-slate-300 p-4 rounded-lg ${className}`}>
    <h3 className="font-bold text-slate-700 mb-3 text-sm uppercase tracking-wider border-b border-slate-200 pb-2">
      {title}
    </h3>
    {children}
  </div>
);

const MetricBox = ({ label, value, subtext }) => (
  <div className="bg-slate-50 border border-slate-300 p-3 rounded text-center">
    <p className="text-xs text-slate-500 uppercase">{label}</p>
    <p className="text-2xl font-mono font-bold text-slate-800 my-1">{value}</p>
    {subtext && <p className="text-xs text-slate-400">{subtext}</p>}
  </div>
);

const Button = ({ label, icon: Icon, primary = false, onClick }) => (
  <button 
    onClick={onClick}
    className={`flex items-center justify-center gap-2 px-4 py-2 rounded border-2 font-medium w-full text-sm
      ${primary 
        ? 'bg-slate-800 text-white border-slate-800 hover:bg-slate-700' 
        : 'bg-white text-slate-700 border-slate-300 hover:bg-slate-50'
      }`}
  >
    {Icon && <Icon size={16} />}
    {label}
  </button>
);

// --- Halaman 1: Dashboard ---
const DashboardPage = () => (
  <div className="space-y-6">
    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
      {/* Ringkasan Proyek */}
      <Card title="Ringkasan Proyek (ViT Traffic Sign)">
        <div className="space-y-3">
          <div className="flex justify-between border-b border-dashed border-slate-300 pb-1">
            <span className="text-slate-600">Total Kelas</span>
            <span className="font-mono font-bold">43 Kelas</span>
          </div>
          <div className="flex justify-between border-b border-dashed border-slate-300 pb-1">
            <span className="text-slate-600">Data Train/Test</span>
            <span className="font-mono font-bold">35k / 12k</span>
          </div>
          <div className="flex justify-between items-center pt-1">
            <span className="text-slate-600">Model Aktif</span>
            <span className="bg-green-100 text-green-800 text-xs px-2 py-1 rounded border border-green-200">
              ViT-Base-Patch16
            </span>
          </div>
        </div>
      </Card>
      
      {/* Last Training */}
       <Card title="Aktivitas Terakhir">
        <div className="text-center py-4">
           <p className="text-slate-500 text-sm">Training terakhir selesai pada:</p>
           <p className="font-mono text-lg font-bold mt-1">25 Jan 2026, 14:30</p>
           <p className="text-xs text-slate-400 mt-2">Durasi: 4h 12m</p>
        </div>
      </Card>
    </div>

    {/* Kartu Metrik */}
    <Card title="Performa Model Terkini">
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <MetricBox label="Validation Loss" value="0.024" subtext="-0.001 dari epoch lalu" />
        <MetricBox label="mAP @0.5" value="94.2%" subtext="Mean Average Precision" />
        <MetricBox label="Precision" value="91.8%" subtext="Positive Predictive Value" />
        <MetricBox label="Recall" value="93.5%" subtext="Sensitivity" />
      </div>
    </Card>
  </div>
);

// --- Halaman 2: Training ---
const TrainingPage = () => (
  <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 h-full">
    {/* Kolom Kiri: Konfigurasi */}
    <div className="lg:col-span-1 space-y-6">
      <Card title="Konfigurasi Training">
        <form className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1">Model Name</label>
            <input type="text" defaultValue="vit_traffic_v3" className="w-full border-2 border-slate-300 p-2 rounded text-sm focus:border-slate-500 outline-none" />
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">Epochs</label>
              <input type="number" defaultValue="100" className="w-full border-2 border-slate-300 p-2 rounded text-sm focus:border-slate-500 outline-none" />
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">Batch Size</label>
              <input type="number" defaultValue="32" className="w-full border-2 border-slate-300 p-2 rounded text-sm focus:border-slate-500 outline-none" />
            </div>
          </div>
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1">Learning Rate</label>
            <input type="text" defaultValue="0.001" className="w-full border-2 border-slate-300 p-2 rounded text-sm focus:border-slate-500 outline-none" />
          </div>
        </form>
      </Card>

      <Card title="Kontrol">
        <div className="space-y-3">
          <Button label="Start Training" icon={Play} primary />
        </div>
      </Card>
    </div>

    {/* Kolom Kanan: Tabel Riwayat */}
    <div className="lg:col-span-2">
      <Card title="Riwayat Training" className="h-full">
        <div className="overflow-x-auto">
          <table className="w-full text-sm text-left">
            <thead className="bg-slate-100 border-b-2 border-slate-300 text-slate-600 uppercase text-xs">
              <tr>
                <th className="p-3">Tanggal</th>
                <th className="p-3">Model ID</th>
                <th className="p-3">Epochs</th>
                <th className="p-3">LR</th>
                <th className="p-3">mAP</th>
                <th className="p-3">Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-200">
              {[1, 2, 3, 4, 5].map((i) => (
                <tr key={i} className="hover:bg-slate-50">
                  <td className="p-3 text-slate-500">2026-01-2{i}</td>
                  <td className="p-3 font-mono">vit_v{i}</td>
                  <td className="p-3">50</td>
                  <td className="p-3 font-mono">1e-4</td>
                  <td className="p-3 font-bold text-slate-700">0.{85 + i}</td>
                  <td className="p-3">
                    <span className={`text-xs px-2 py-1 rounded border ${i === 5 ? 'bg-yellow-50 border-yellow-200 text-yellow-700' : 'bg-green-50 border-green-200 text-green-700'}`}>
                      {i === 5 ? 'Running' : 'Completed'}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Card>
    </div>
  </div>
);

// --- Halaman 3: Dataset Explorer ---
const DatasetPage = () => (
  <div className="space-y-6">
    {/* Statistik & Info */}

    {/* Grid Preview */}
    <Card title="Preview Sampel Data (Placeholder)">
      <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-4">
        {[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12].map((i) => (
          <div key={i} className="group relative aspect-square bg-slate-100 border-2 border-dashed border-slate-300 rounded flex flex-col items-center justify-center hover:border-slate-500 cursor-pointer transition-colors">
            <ImageIcon className="text-slate-300 mb-2 group-hover:text-slate-500" size={32} />
            <span className="text-xs text-slate-400 font-mono">img_{i}.jpg</span>
            <div className="absolute top-2 right-2 w-3 h-3 bg-red-400 rounded-full border border-white" title="Annotated"></div>
          </div>
        ))}
      </div>
      <div className="mt-4 flex justify-center">
        <button className="text-sm text-slate-500 hover:text-slate-800 underline">Muat lebih banyak...</button>
      </div>
    </Card>
  </div>
);

// --- Layout Utama ---
export default function App() {
  const [activePage, setActivePage] = useState('dashboard');

  const renderContent = () => {
    switch (activePage) {
      case 'dashboard': return <DashboardPage />;
      case 'training': return <TrainingPage />;
      case 'dataset': return <DatasetPage />;
      default: return <DashboardPage />;
    }
  };

  return (
    <div className="flex h-screen bg-slate-100 font-sans text-slate-800 overflow-hidden selection:bg-slate-200">
      
      {/* Sidebar Navigasi */}
      <aside className="w-64 bg-white border-r-2 border-slate-200 flex flex-col flex-shrink-0 z-20">
        <div className="h-16 flex items-center px-6 border-b-2 border-slate-100">
          <div className="w-6 h-6 bg-slate-800 rounded mr-3"></div>
          <span className="font-bold text-lg tracking-tight">ViT Traffic<span className="text-slate-400">Net</span></span>
        </div>

        <nav className="flex-1 p-4 space-y-1">
          <button 
            onClick={() => setActivePage('dashboard')}
            className={`w-full flex items-center gap-3 px-4 py-3 text-sm font-medium rounded transition-colors ${activePage === 'dashboard' ? 'bg-slate-100 text-slate-900 border border-slate-300' : 'text-slate-500 hover:bg-slate-50 hover:text-slate-700'}`}
          >
            <LayoutDashboard size={18} />
            Dashboard Overview
          </button>
          <button 
            onClick={() => setActivePage('training')}
            className={`w-full flex items-center gap-3 px-4 py-3 text-sm font-medium rounded transition-colors ${activePage === 'training' ? 'bg-slate-100 text-slate-900 border border-slate-300' : 'text-slate-500 hover:bg-slate-50 hover:text-slate-700'}`}
          >
            <Settings size={18} />
            Training & Model
          </button>
          <button 
            onClick={() => setActivePage('dataset')}
            className={`w-full flex items-center gap-3 px-4 py-3 text-sm font-medium rounded transition-colors ${activePage === 'dataset' ? 'bg-slate-100 text-slate-900 border border-slate-300' : 'text-slate-500 hover:bg-slate-50 hover:text-slate-700'}`}
          >
            <Database size={18} />
            Dataset Explorer
          </button>
        </nav>

        <div className="p-4 border-t border-slate-200">
          <div className="flex items-center gap-3 px-2">
            <div className="w-8 h-8 rounded-full bg-slate-300"></div>
            <div>
              <p className="text-xs font-bold">Admin User</p>
              <p className="text-[10px] text-slate-400">Researcher</p>
            </div>
          </div>
        </div>
      </aside>

      {/* Area Konten */}
      <main className="flex-1 flex flex-col min-w-0 bg-slate-50">
        {/* Header Sederhana */}
        <header className="h-16 bg-white border-b border-slate-200 flex items-center justify-between px-8 flex-shrink-0">
          <h2 className="text-xl font-bold text-slate-700 capitalize">
            {activePage === 'dashboard' ? 'System Overview' : activePage.replace('_', ' ')}
          </h2>
        </header>

        {/* Konten Scrollable */}
        <div className="flex-1 overflow-auto p-8">
          <div className="max-w-6xl mx-auto">
            {renderContent()}
          </div>
        </div>
      </main>
    </div>
  );
}
```