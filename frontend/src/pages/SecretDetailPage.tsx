import { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';

const PROJECT = 'sample';
const API_BASE = `/api/team/${PROJECT}`;

export default function SecretDetailPage() {
    const { id } = useParams();
    const navigate = useNavigate();
    const [value, setValue] = useState('');
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        if (!id) return;
        setLoading(true);
        setError(null);
        fetch(`${API_BASE}/secret/${encodeURIComponent(id)}`)
            .then(res => {
                if (!res.ok) throw new Error('Secret not found');
                return res.json();
            })
            .then(data => setValue(data.value))
            .catch(err => setError(err.message || 'Unknown error'))
            .finally(() => setLoading(false));
    }, [id]);

    if (!id) {
        return (
            <div className="flex flex-col items-center justify-center h-full py-16">
                <h2 className="text-2xl font-bold text-orange-700 mb-4">No Secret Key Provided</h2>
                <button className="mt-4 px-4 py-2 bg-gray-300 rounded" onClick={() => navigate('/secrets')}>Back to List</button>
            </div>
        );
    }

    return (
        <div className="flex flex-col items-center justify-center h-full py-16 w-full max-w-lg mx-auto">
            <h2 className="text-3xl font-bold text-orange-700 mb-4">Secret Details</h2>
            <div className="bg-white rounded shadow p-6 w-full">
                {loading ? (
                    <div>Loading...</div>
                ) : error ? (
                    <div className="text-red-600">{error}</div>
                ) : (
                    <>
                        <div className="mb-4">
                            <span className="font-semibold">Key:</span> {id}
                        </div>
                        <div className="mb-4">
                            <span className="font-semibold">Value:</span> <span className="font-mono bg-gray-100 px-2 py-1 rounded">{value}</span>
                        </div>
                    </>
                )}
                <button className="mt-4 px-4 py-2 bg-gray-300 rounded" onClick={() => navigate('/secrets')}>Back to List</button>
            </div>
        </div>
    );
} 