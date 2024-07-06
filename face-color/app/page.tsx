import ImageUpload from '../components/ImageUpload'
import ImageList from '../components/ImageList'

export default function Home() {
    return (
        <div>
            <h1>Image Upload and Processing</h1>
            <ImageUpload />
            <ImageList />
        </div>
    )
}