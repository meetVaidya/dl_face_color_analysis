'use client'

import React, { useEffect, useState } from 'react'
import { listImages } from '../utils/imageHandling'

type Image = {
    name: string;
    publicUrl: string;
    metadata: { [key: string]: any };
}

export default function ImageList() {
    const [images, setImages] = useState<Image[]>([])

    useEffect(() => {
        async function fetchImages() {
            const imageList = await listImages()
            if (imageList) {
                setImages(imageList)
            }
        }
        fetchImages()
    }, [])

    return (
        <div>
            <h2>Uploaded Images</h2>
            <ul>
                {images.map((image, index) => (
                    <li key={index}>
                        <img src={image.publicUrl} alt={image.name} style={{ width: '100px', height: '100px', objectFit: 'cover' }} />
                        <p>Name: {image.name}</p>
                        <p>Upload Date: {image.metadata.uploadedAt}</p>
                    </li>
                ))}
            </ul>
        </div>
    )
}