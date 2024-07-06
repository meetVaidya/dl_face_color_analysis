'use client'

import React, { useState, useEffect } from 'react'
import { uploadImage } from '../utils/imageHandling'
import { supabase } from '../lib/supabase'

export default function ImageUpload() {
    const [file, setFile] = useState<File | null>(null)
    const [uploading, setUploading] = useState(false)
    const [session, setSession] = useState(null)

    useEffect(() => {
        supabase.auth.getSession().then(({ data: { session } }) => {
            setSession(session)
        })

        const {
            data: { subscription },
        } = supabase.auth.onAuthStateChange((_event, session) => {
            setSession(session)
        })

        return () => subscription.unsubscribe()
    }, [])

    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files) {
            setFile(e.target.files[0])
        }
    }

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault()
        if (file && session) {
            setUploading(true)
            const metadata = { uploadedAt: new Date().toISOString() }
            const imageUrl = await uploadImage(file, metadata)
            setUploading(false)
            if (imageUrl) {
                console.log('Image uploaded successfully. Public URL:', imageUrl)
            }
        }
    }

    if (!session) {
        return <div>Please sign in to upload images.</div>
    }

    return (
        <form onSubmit={handleSubmit}>
            <input type="file" onChange={handleFileChange} disabled={uploading} />
            <button type="submit" disabled={!file || uploading}>
                {uploading ? 'Uploading...' : 'Upload'}
            </button>
        </form>
    )
}