import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';

const PROJECT = 'sample';
const API_BASE = `/api/team/${PROJECT}`;

export default function SecretsListPage() {
    const [secrets, setSecrets] = useState<{ [key: string]: string }>({});
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const navigate = useNavigate();

    const fetchSecrets = async () => {
        setLoading(true);
        setError(null);
        try {
            const res = await fetch(`${API_BASE}/secrets`);
            if (!res.ok) throw new Error('Failed to fetch secrets');
            const data = await res.json();
            setSecrets(data);
        } catch (err: any) {
            setError(err.message || 'Unknown error');
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchSecrets();
    }, []);

    const handleDelete = async (key: string) => {
        if (!window.confirm(`Delete secret "${key}"?`)) return;
        try {
            const res = await fetch(`${API_BASE}/secret/${encodeURIComponent(key)}`, { method: 'DELETE' });
            if (!res.ok) throw new Error('Failed to delete secret');
            fetchSecrets();
        } catch (err: any) {
            alert(err.message || 'Delete failed');
        }
    };

    return (
        <div className="flex flex-col items-center justify-center h-full py-16 w-full max-w-2xl mx-auto bg-gradient-to-br from-[#4FC3F7]/20 to-[#1565C0]/10">
            <h2 className="text-3xl font-bold text-[#1565C0] mb-4">Secrets & Config</h2>
            <div className="w-full bg-white rounded shadow p-6 mb-8">
                {loading ? (
                    <div>Loading...</div>
                ) : error ? (
                    <div className="text-red-600">{error}</div>
                ) : (
                    <table className="w-full text-left">
                        <thead>
                            <tr className="bg-[#4FC3F7]/30">
                                <th className="py-2 px-4 text-[#1565C0]">Key</th>
                                <th className="py-2 px-4 text-[#1565C0]">Value</th>
                                <th className="py-2 px-4 text-[#1565C0]">Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            {Object.entries(secrets).map(([key, value]) => (
                                <tr key={key} className="border-t">
                                    <td className="py-2 px-4 font-semibold">{key}</td>
                                    <td className="py-2 px-4 font-mono">••••••••</td>
                                    <td className="py-2 px-4">
                                        <button
                                            className="text-[#1565C0] hover:underline mr-2"
                                            onClick={() => navigate(`/secrets/${encodeURIComponent(key)}`)}
                                        >
                                            View
                                        </button>
                                        <button
                                            className="text-[#1976D2] hover:underline mr-2"
                                            onClick={() => navigate(`/secrets/new?key=${encodeURIComponent(key)}`)}
                                        >
                                            Edit
                                        </button>
                                        <button
                                            className="text-[#D32F2F] hover:underline"
                                            onClick={() => handleDelete(key)}
                                        >
                                            Delete
                                        </button>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                )}
            </div>
            <button
                className="px-4 py-2 bg-[#1565C0] text-white rounded hover:bg-[#1976D2] transition-colors font-semibold shadow"
                onClick={() => navigate('/secrets/new')}
            >
                Add New Secret
            </button>
        </div>
    );
} 