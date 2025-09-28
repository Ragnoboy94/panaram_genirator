import cv2, numpy as np
from pathlib import Path
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse

app = FastAPI()

def read_from_upload(upload: UploadFile):
    data = np.frombuffer(upload.file.read(), np.uint8)
    return cv2.imdecode(data, cv2.IMREAD_COLOR)

def auto_crop_largest_rectangle(img):
    nonblack = np.any(img>0, axis=2).astype(np.uint8)
    H,W = nonblack.shape
    heights = np.zeros(W, dtype=int)
    best=(0,0,0,0); area=0
    for y in range(H):
        row = nonblack[y]; heights = (heights+row)*row
        st=[]; x=0
        while x<=W:
            h=heights[x] if x<W else 0
            if not st or h>=heights[st[-1]]: st.append(x); x+=1
            else:
                top=st.pop(); hh=heights[top]
                left=st[-1]+1 if st else 0; right=x-1
                a=hh*(right-left+1)
                if a>area: area=a; y1=y+1; y0=y1-hh; best=(y0,y1,left,right+1)
    y0,y1,x0,x1 = best
    if (y1-y0)<10 or (x1-x0)<10: return img
    return img[y0:y1, x0:x1]

@app.post("/stitch")
async def stitch(left: UploadFile = File(...),
                 center: UploadFile = File(...),
                 right: UploadFile = File(...)):
    imgs = [read_from_upload(left), read_from_upload(center), read_from_upload(right)]

    for mode in (cv2.Stitcher_PANORAMA, cv2.Stitcher_SCANS):
        stitcher = cv2.Stitcher_create(mode)
        stitcher.setPanoConfidenceThresh(0.6)
        try:
            stitcher.setWarper(cv2.detail_CylindricalWarper())
            stitcher.setWaveCorrection(True)
        except Exception:
            pass
        status, pano = stitcher.stitch(imgs)
        if status == cv2.STITCHER_OK and pano is not None:
            cropped = auto_crop_largest_rectangle(pano)
            out = Path("/app/panorama.jpg")
            ok = cv2.imencode(".jpg", cropped, [int(cv2.IMWRITE_JPEG_QUALITY),95])[1]
            out.write_bytes(ok.tobytes())
            return FileResponse(out, media_type="image/jpeg")
    return {"error": "stitch failed"}
