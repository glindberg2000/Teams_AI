import { useEffect, useState } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';

const PROJECT = 'sample';
const API_BASE = `/api/team/${PROJECT}`;

export default function SecretFormPage() {
    const navigate = useNavigate();
    const [searchParams] = useSearchParams();
    const keyParam = searchParams.get('key') || '';
    const isEdit = Boolean(keyParam);
    const [key, setKey] = useState(keyParam);
    const [value, setValue] = useState('');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        if (isEdit && key) {
            setLoading(true);
            fetch(`${API_BASE}/secret/${encodeURIComponent(key)}`)
                .then(res => {
                    if (!res.ok) throw new Error('Failed to fetch secret');
                    return res.json();
                })
                .then(data => setValue(data.value))
                .catch(err => setError(err.message || 'Unknown error'))
                .finally(() => setLoading(false));
        }
    }, [isEdit, key]);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);
        setError(null);
        try {
            const body = JSON.stringify({ [key]: value });
            const res = await fetch(`${API_BASE}/secret`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body,
            });
            if (!res.ok) throw new Error('Failed to save secret');
            navigate('/secrets');
        } catch (err: any) {
            setError(err.message || 'Unknown error');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="flex flex-col items-center justify-center h-full py-16 w-full max-w-lg mx-auto">
            <h2 className="text-3xl font-bold text-pink-700 mb-4">{isEdit ? 'Edit Secret' : 'Add Secret'}</h2>
            <form onSubmit={handleSubmit} className="bg-white rounded shadow p-6 w-full flex flex-col gap-4">
                <div>
                    <label className="block font-semibold mb-1">Key</label>
                    <input
                        name="key"
                        type="text"
                        className="w-full border rounded px-3 py-2"
                        value={key}
                        onChange={e => setKey(e.target.value)}
                        required
                        disabled={isEdit}
                    />
                </div>
                <div>
                    <label className="block font-semibold mb-1">Value</label>
                    <input
                        name="value"
                        type="password"
                        className="w-full border rounded px-3 py-2 font-mono"
                        value={value}
                        onChange={e => setValue(e.target.value)}
                        required
                    />
                </div>
                {error && <div className="text-red-600">{error}</div>}
                <div className="flex gap-4 mt-4">
                    <button
                        type="submit"
                        className="px-4 py-2 bg-pink-600 text-white rounded hover:bg-pink-700 transition-colors"
                        disabled={loading}
                    >
                        {isEdit ? 'Update' : 'Create'}
                    </button>
                    <button
                        type="button"
                        className="px-4 py-2 bg-gray-300 rounded"
                        onClick={() => navigate('/secrets')}
                        disabled={loading}
                    >
                        Cancel
                    </button>
                </div>
            </form>
        </div>
    );
} 