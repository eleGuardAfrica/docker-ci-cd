from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from ayrshare import SocialPost
import os
from pathlib import Path

social = SocialPost("3F73D951-0CF94226-B0C5D651-2ABAB5F3")

app = FastAPI()

# Get the public folder path
PUBLIC_FOLDER = Path(__file__).parent.parent / "public"

class ShareRequest(BaseModel):
    post: str
    platforms: list


def post_now(post: str, platforms: list):
    json_data = {
        "post": post,
        "platforms": platforms
    }
    response = social.post(json_data)
    return response  # IMPORTANT: return this


def get_file_size(file_path: Path) -> str:
    """Convert file size to human readable format"""
    size = file_path.stat().st_size
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024
    return f"{size:.2f} TB"


@app.get("/")
def hello():
    return {"message": "Hello, Allord!"}


@app.get("/files", response_class=HTMLResponse)
def list_files():
    """Serve a nice UI to list and download files from public folder"""
    try:
        files = []
        if PUBLIC_FOLDER.exists():
            for file_path in PUBLIC_FOLDER.iterdir():
                if file_path.is_file():
                    files.append({
                        "name": file_path.name,
                        "size": get_file_size(file_path),
                        "path": f"/download/{file_path.name}"
                    })
        
        files.sort(key=lambda x: x["name"])
        
        files_html = ""
        if files:
            for file in files:
                files_html += f"""
                <div class="file-item">
                    <div class="file-info">
                        <h3>{file['name']}</h3>
                        <p class="file-size">Size: {file['size']}</p>
                    </div>
                    <a href="{file['path']}" class="download-btn" download>
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                            <polyline points="7 10 12 15 17 10"></polyline>
                            <line x1="12" y1="15" x2="12" y2="3"></line>
                        </svg>
                        Download
                    </a>
                </div>
                """
        else:
            files_html = '<p class="no-files">No files available</p>'
        
        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>File Download Center</title>
            <style>
                * {{
                    margin: 0;
                    padding: 0;
                    box-sizing: border-box;
                }}
                
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    min-height: 100vh;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    padding: 20px;
                }}
                
                .container {{
                    background: white;
                    border-radius: 15px;
                    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
                    max-width: 800px;
                    width: 100%;
                    padding: 40px;
                    animation: slideIn 0.5s ease-out;
                }}
                
                @keyframes slideIn {{
                    from {{
                        opacity: 0;
                        transform: translateY(20px);
                    }}
                    to {{
                        opacity: 1;
                        transform: translateY(0);
                    }}
                }}
                
                h1 {{
                    color: #333;
                    margin-bottom: 10px;
                    font-size: 2.5em;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;
                    background-clip: text;
                }}
                
                .subtitle {{
                    color: #666;
                    margin-bottom: 30px;
                    font-size: 1.1em;
                }}
                
                .files-container {{
                    display: flex;
                    flex-direction: column;
                    gap: 15px;
                }}
                
                .file-item {{
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    padding: 20px;
                    background: #f8f9fa;
                    border-radius: 10px;
                    border-left: 4px solid #667eea;
                    transition: all 0.3s ease;
                    animation: fadeIn 0.6s ease-out;
                }}
                
                @keyframes fadeIn {{
                    from {{
                        opacity: 0;
                        transform: translateX(-10px);
                    }}
                    to {{
                        opacity: 1;
                        transform: translateX(0);
                    }}
                }}
                
                .file-item:hover {{
                    background: #f0f1ff;
                    transform: translateX(5px);
                    box-shadow: 0 5px 15px rgba(102, 126, 234, 0.1);
                }}
                
                .file-info {{
                    flex: 1;
                }}
                
                .file-info h3 {{
                    color: #333;
                    margin-bottom: 5px;
                    word-break: break-all;
                }}
                
                .file-size {{
                    color: #999;
                    font-size: 0.9em;
                    margin: 0;
                }}
                
                .download-btn {{
                    display: flex;
                    align-items: center;
                    gap: 8px;
                    padding: 10px 20px;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    text-decoration: none;
                    border-radius: 8px;
                    font-weight: 600;
                    transition: all 0.3s ease;
                    white-space: nowrap;
                    margin-left: 20px;
                }}
                
                .download-btn:hover {{
                    transform: translateY(-2px);
                    box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
                }}
                
                .download-btn:active {{
                    transform: translateY(0);
                }}
                
                .no-files {{
                    text-align: center;
                    color: #999;
                    padding: 40px 20px;
                    font-size: 1.1em;
                }}
                
                .footer {{
                    margin-top: 30px;
                    text-align: center;
                    color: #999;
                    font-size: 0.9em;
                    border-top: 1px solid #eee;
                    padding-top: 20px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>📁 File Download Center</h1>
                <p class="subtitle">Download your files with ease</p>
                
                <div class="files-container">
                    {files_html}
                </div>
                
                <div class="footer">
                    <p>Total files available: <strong>{len(files)}</strong></p>
                </div>
            </div>
        </body>
        </html>
        """
        return html_content
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/download/{file_name}")
def download_file(file_name: str):
    """Download a specific file from public folder"""
    try:
        file_path = PUBLIC_FOLDER / file_name
        
        # Security check: prevent directory traversal
        if not file_path.is_relative_to(PUBLIC_FOLDER):
            raise HTTPException(status_code=403, detail="Access denied")
        
        if not file_path.exists() or not file_path.is_file():
            raise HTTPException(status_code=404, detail="File not found")
        
        return FileResponse(
            path=file_path,
            filename=file_name,
            media_type='application/octet-stream'
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/files")
def get_files_json():
    """Get list of files in JSON format"""
    try:
        files = []
        if PUBLIC_FOLDER.exists():
            for file_path in PUBLIC_FOLDER.iterdir():
                if file_path.is_file():
                    files.append({
                        "name": file_path.name,
                        "size": file_path.stat().st_size,
                        "size_formatted": get_file_size(file_path),
                        "download_url": f"/download/{file_path.name}"
                    })
        
        files.sort(key=lambda x: x["name"])
        return {"files": files, "total": len(files)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/share")
def share_post(req: ShareRequest):
    response = post_now(req.post, req.platforms)
    return {"post_status": response}
