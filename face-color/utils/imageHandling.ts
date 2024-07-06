import { supabase } from '../lib/supabase'

const BUCKET_NAME = process.env.NEXT_PUBLIC_SUPABASE_STORAGE_BUCKET || 'images'

export async function uploadImage(file: File, metadata: object = {}) {
    console.log(`Attempting to upload image to bucket: ${BUCKET_NAME}`)

    const fileName = `image-${Date.now()}.jpg`

    const { data, error } = await supabase.storage
        .from(BUCKET_NAME)
        .upload(fileName, file, {
            upsert: true,
            contentType: file.type,
            cacheControl: '3600',
        })

    if (error) {
        console.error('Error uploading image:', error)
        console.error('Error details:', JSON.stringify(error, null, 2))
        return null
    }

    console.log('Image uploaded successfully:', data)

    // Store metadata
    const { error: metadataError } = await supabase
        .from('image_metadata')
        .insert({ file_name: fileName, metadata })

    if (metadataError) {
        console.error('Error storing metadata:', metadataError)
        console.error('Error details:', JSON.stringify(metadataError, null, 2))
    }

    return getPublicUrl(data.path)
}

export function getPublicUrl(path: string) {
    const { data } = supabase.storage
        .from(BUCKET_NAME)
        .getPublicUrl(path)

    return data.publicUrl
}

export async function listImages() {
    const { data: files, error: filesError } = await supabase.storage
        .from(BUCKET_NAME)
        .list()

    if (filesError) {
        console.error('Error listing images:', filesError)
        return null
    }

    const { data: metadata, error: metadataError } = await supabase
        .from('image_metadata')
        .select('*')

    if (metadataError) {
        console.error('Error fetching metadata:', metadataError)
    }

    return files.map(file => ({
        name: file.name,
        publicUrl: getPublicUrl(file.name),
        metadata: metadata?.find(m => m.file_name === file.name)?.metadata || {}
    }))
}