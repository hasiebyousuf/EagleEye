'use client'

import { useState, useEffect } from 'react'
import { apiPost, apiGet } from '@/lib/api'
import { useRouter } from 'next/navigation'
import type { Workspace } from '@/types'

export default function OnboardingPage() {
  const [name, setName] = useState('')
  const [budget, setBudget] = useState('')
  const [nameError, setNameError] = useState<string | null>(null)
  const [budgetError, setBudgetError] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)
  const router = useRouter()

  useEffect(() => {
    apiGet<Workspace>('/workspace')
      .then(() => router.replace('/dashboard'))
      .catch(() => {})
  }, [router])

  function validate(): boolean {
    let valid = true
    if (!name.trim()) {
      setNameError('Workspace name is required')
      valid = false
    } else {
      setNameError(null)
    }
    const budgetNum = parseFloat(budget)
    if (!budget || isNaN(budgetNum) || budgetNum <= 0) {
      setBudgetError('Budget must be a positive number')
      valid = false
    } else {
      setBudgetError(null)
    }
    return valid
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    if (!validate()) return
    setLoading(true)
    try {
      await apiPost('/workspace', { name: name.trim(), budget: parseFloat(budget) })
      router.push('/dashboard')
    } catch {
      setLoading(false)
    }
  }

  return (
    <main style={{ maxWidth: 480, margin: '80px auto', padding: '0 16px' }}>
      <h1>Set up your workspace</h1>
      <p>Tell us about your business and budget so EagleEye can tailor its recommendations.</p>
      <form onSubmit={handleSubmit}>
        <div style={{ marginBottom: 20 }}>
          <label htmlFor="name">Workspace name</label>
          <input
            id="name"
            type="text"
            value={name}
            onChange={e => setName(e.target.value)}
            placeholder="e.g. My Ecommerce Store"
            style={{ display: 'block', width: '100%', marginTop: 4 }}
          />
          {nameError && <p style={{ color: 'red', fontSize: 14 }}>{nameError}</p>}
        </div>
        <div style={{ marginBottom: 20 }}>
          <label htmlFor="budget">Total budget (USD)</label>
          <input
            id="budget"
            type="number"
            value={budget}
            onChange={e => setBudget(e.target.value)}
            placeholder="e.g. 5000"
            min="0.01"
            step="any"
            style={{ display: 'block', width: '100%', marginTop: 4 }}
          />
          {budgetError && <p style={{ color: 'red', fontSize: 14 }}>{budgetError}</p>}
        </div>
        <button type="submit" disabled={loading}>
          {loading ? 'Creating workspace…' : 'Get started'}
        </button>
      </form>
    </main>
  )
}
