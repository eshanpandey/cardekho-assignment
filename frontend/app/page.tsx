'use client';

import { useState } from 'react';

interface Recommendation {
  variant_id: number;
  confidence_score: number;
  match_explanation: string;
  strengths: string[];
  tradeoffs: string[];
}

interface RecommendationResponse {
  recommendations: Recommendation[];
  count: number;
  total_candidates: number;
  reasoning_summary?: string;
}

export default function Home() {
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState<RecommendationResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResults(null);

    const formData = new FormData(e.currentTarget);
    const budgetMin = parseFloat(formData.get('budget_min') as string);
    const budgetMax = parseFloat(formData.get('budget_max') as string);

    // Validate budget range
    if (budgetMin < 50000 || budgetMax < 50000) {
      setError('Budget values must be at least ₹50,000');
      setLoading(false);
      return;
    }

    if (budgetMax <= budgetMin) {
      setError('Maximum budget must be greater than minimum budget');
      setLoading(false);
      return;
    }

    const preferences: any = {
      user_id: 1,
      budget_min: budgetMin,
      budget_max: budgetMax,
      priority_fuel_eff: formData.get('priority_fuel_eff') as string,
      priority_safety: formData.get('priority_safety') as string,
      priority_performance: formData.get('priority_performance') as string,
      priority_comfort: formData.get('priority_comfort') as string,
    };

    // Only add optional fields if they have values
    const fuelType = formData.get('fuel_type_constraint') as string;
    const transmission = formData.get('transmission_pref') as string;
    
    if (fuelType && fuelType !== '') {
      preferences.fuel_type_constraint = fuelType;
    }
    if (transmission && transmission !== '') {
      preferences.transmission_pref = transmission;
    }

    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || '/api';
      const response = await fetch(`${apiUrl}/recommendations`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(preferences),
      });

      if (!response.ok) throw new Error(`API error: ${response.status}`);

      const data = await response.json();
      setResults(data);
      
      // Scroll to results
      setTimeout(() => {
        document.getElementById('results')?.scrollIntoView({ behavior: 'smooth' });
      }, 100);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-6xl mx-auto px-4 py-6">
          <h1 className="text-3xl font-bold text-gray-900">CarMatch</h1>
          <p className="text-gray-600 mt-1">Find your perfect car with AI-powered recommendations</p>
        </div>
      </header>

      <main className="max-w-6xl mx-auto px-4 py-8">
        {/* Preference Form */}
        <div className="bg-white rounded-lg shadow-md p-6 mb-8">
          <h2 className="text-xl font-semibold text-gray-900 mb-6">Your Preferences</h2>
          
          <form onSubmit={handleSubmit} className="space-y-6">
            {/* Budget */}
            <div>
              <h3 className="text-sm font-medium text-gray-700 mb-3">Budget Range</h3>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm text-gray-600 mb-1">Minimum (₹)</label>
                  <input
                    type="number"
                    name="budget_min"
                    defaultValue="500000"
                    min="50000"
                    step="50000"
                    required
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white text-gray-900"
                  />
                </div>
                <div>
                  <label className="block text-sm text-gray-600 mb-1">Maximum (₹)</label>
                  <input
                    type="number"
                    name="budget_max"
                    defaultValue="1500000"
                    min="50000"
                    step="50000"
                    required
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white text-gray-900"
                  />
                </div>
              </div>
            </div>

            {/* Priorities */}
            <div>
              <h3 className="text-sm font-medium text-gray-700 mb-3">Priorities</h3>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div>
                  <label className="block text-sm text-gray-600 mb-1">Fuel Efficiency</label>
                  <select
                    name="priority_fuel_eff"
                    defaultValue="high"
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white text-gray-900"
                  >
                    <option value="low">Low</option>
                    <option value="medium">Medium</option>
                    <option value="high">High</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm text-gray-600 mb-1">Safety</label>
                  <select
                    name="priority_safety"
                    defaultValue="high"
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white text-gray-900"
                  >
                    <option value="low">Low</option>
                    <option value="medium">Medium</option>
                    <option value="high">High</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm text-gray-600 mb-1">Performance</label>
                  <select
                    name="priority_performance"
                    defaultValue="medium"
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white text-gray-900"
                  >
                    <option value="low">Low</option>
                    <option value="medium">Medium</option>
                    <option value="high">High</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm text-gray-600 mb-1">Comfort</label>
                  <select
                    name="priority_comfort"
                    defaultValue="medium"
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white text-gray-900"
                  >
                    <option value="low">Low</option>
                    <option value="medium">Medium</option>
                    <option value="high">High</option>
                  </select>
                </div>
              </div>
            </div>

            {/* Constraints */}
            <div>
              <h3 className="text-sm font-medium text-gray-700 mb-3">Preferences (Optional)</h3>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm text-gray-600 mb-1">Fuel Type</label>
                  <select
                    name="fuel_type_constraint"
                    defaultValue="petrol"
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white text-gray-900"
                  >
                    <option value="">Any</option>
                    <option value="petrol">Petrol</option>
                    <option value="diesel">Diesel</option>
                    <option value="electric">Electric</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm text-gray-600 mb-1">Transmission</label>
                  <select
                    name="transmission_pref"
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white text-gray-900"
                  >
                    <option value="">Any</option>
                    <option value="manual">Manual</option>
                    <option value="automatic">Automatic</option>
                    <option value="cvt">CVT</option>
                  </select>
                </div>
              </div>
            </div>

            {/* Submit Button */}
            <button
              type="submit"
              disabled={loading}
              className="w-full bg-blue-600 text-white py-3 px-6 rounded-md font-medium hover:bg-blue-700 transition disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? 'Finding matches...' : 'Get Recommendations'}
            </button>
          </form>
        </div>

        {/* Loading State */}
        {loading && (
          <div className="text-center py-12">
            <div className="inline-block animate-spin rounded-full h-12 w-12 border-4 border-gray-200 border-t-blue-600"></div>
            <p className="mt-4 text-gray-600">Finding your perfect matches...</p>
          </div>
        )}

        {/* Error Message */}
        {error && (
          <div className="bg-red-50 border border-red-200 rounded-md p-4 text-red-800 mb-8">
            Error: {error}. Make sure the API server is running on http://localhost:8000
          </div>
        )}

        {/* Results */}
        {results && (
          <div id="results">
            <h2 className="text-2xl font-semibold text-gray-900 mb-6">
              Your Recommendations ({results.count} matches)
            </h2>
            <div className="space-y-6">
              {results.recommendations.map((rec, index) => (
                <div
                  key={rec.variant_id}
                  className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition"
                >
                  <div className="flex justify-between items-start mb-4">
                    <div>
                      <span className="inline-block bg-blue-100 text-blue-800 text-xs font-semibold px-2 py-1 rounded mb-2">
                        #{index + 1}
                      </span>
                      <h3 className="text-lg font-semibold text-gray-900">
                        Recommendation {index + 1}
                      </h3>
                    </div>
                    <div className="text-right">
                      <div className="text-2xl font-bold text-blue-600">
                        {rec.confidence_score}
                      </div>
                      <div className="text-xs text-gray-500">Match Score</div>
                    </div>
                  </div>

                  <p className="text-gray-700 mb-4 leading-relaxed">
                    {rec.match_explanation}
                  </p>

                  {rec.strengths && rec.strengths.length > 0 && (
                    <div className="mb-4">
                      <h4 className="text-sm font-semibold text-gray-900 mb-2">
                        Strengths
                      </h4>
                      <ul className="space-y-1">
                        {rec.strengths.map((strength, i) => (
                          <li key={i} className="text-sm text-gray-700 flex items-start">
                            <span className="text-green-500 mr-2">✓</span>
                            <span>{strength}</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}

                  {rec.tradeoffs && rec.tradeoffs.length > 0 && (
                    <div>
                      <h4 className="text-sm font-semibold text-gray-900 mb-2">
                        Considerations
                      </h4>
                      <ul className="space-y-1">
                        {rec.tradeoffs.map((tradeoff, i) => (
                          <li key={i} className="text-sm text-gray-600 flex items-start">
                            <span className="text-yellow-500 mr-2">•</span>
                            <span>{tradeoff}</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
