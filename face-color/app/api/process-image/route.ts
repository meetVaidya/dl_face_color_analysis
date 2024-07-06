import { NextResponse } from 'next/server'
import { supabase } from '../../../lib/supabase'

export async function POST(request: Request) {
    const { imageId } = await request.json()

    const { data, error } = await supabase
        .from('images')
        .select('url')
        .eq('id', imageId)
        .single()

    if (error) {
        return NextResponse.json({ error: 'Error retrieving image URL' }, { status: 500 })
    }

    // Here you would typically call your ML model API
    console.log('Processing image:', data.url)

    return NextResponse.json({ message: 'Image processed successfully' })
}