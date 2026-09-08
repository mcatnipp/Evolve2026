// Evolve leadership headshot template.
// Usage: headshot-template <input image> <output dir> <slug>
// Produces <slug>-800.jpg (800x1000) and <slug>-400.jpg (400x500):
//   1. Vision face detection sets a consistent 4:5 crop (face ~32% of frame height, headroom above).
//   2. Vision person segmentation lifts the subject onto a neutral studio backdrop (radial gray gradient).
//   3. Black-and-white grade: CIPhotoEffectMono, gentle contrast, light unsharp mask.
// Build once:  swiftc -O scripts/headshot-template.swift -o /tmp/headshot-template
import Foundation
import Vision
import CoreImage
import CoreImage.CIFilterBuiltins

let args = CommandLine.arguments
guard args.count >= 4 else { FileHandle.standardError.write("usage: headshot-template <input> <outdir> <slug>\n".data(using: .utf8)!); exit(64) }
let input = URL(fileURLWithPath: args[1])
let outDir = URL(fileURLWithPath: args[2], isDirectory: true)
let slug = args[3]

guard let source = CIImage(contentsOf: input)?.oriented(.up) else { print("cannot read \(input.path)"); exit(1) }
let W = source.extent.width, H = source.extent.height

// ---- 1. Face detection ----
let handler = VNImageRequestHandler(ciImage: source, options: [:])
let faceReq = VNDetectFaceRectanglesRequest()
let segReq = VNGeneratePersonSegmentationRequest()
segReq.qualityLevel = .accurate
segReq.outputPixelFormat = kCVPixelFormatType_OneComponent8
do { try handler.perform([faceReq, segReq]) } catch { print("vision failed: \(error)"); exit(2) }

var faceRect = CGRect(x: W * 0.3, y: H * 0.35, width: W * 0.4, height: W * 0.4)   // fallback: centered
var faceFound = false
if let f = faceReq.results?.sorted(by: { $0.boundingBox.width > $1.boundingBox.width }).first {
    let b = f.boundingBox   // normalized, origin bottom-left
    faceRect = CGRect(x: b.minX * W, y: b.minY * H, width: b.width * W, height: b.height * H)
    faceFound = true
}

// ---- 2. Crop geometry (4:5). Face height ~ 32% of frame; face center at 44% from the top. ----
var cropH = faceRect.height / 0.32
var cropW = cropH * 0.8
// Shrink to fit inside the source; never extend beyond real pixels.
if cropW > W { cropW = W; cropH = cropW / 0.8 }
if cropH > H { cropH = H; cropW = cropH * 0.8 }
let faceCX = faceRect.midX, faceCY = faceRect.midY
var cropX = faceCX - cropW / 2
var cropTop = faceCY + cropH * 0.44           // CI coordinates: y grows upward
var cropY = cropTop - cropH
cropX = min(max(cropX, 0), W - cropW)
cropY = min(max(cropY, 0), H - cropH)
let crop = CGRect(x: cropX, y: cropY, width: cropW, height: cropH).integral

// ---- 3. Person mask -> composite onto studio backdrop ----
var composed = source
if let m = segReq.results?.first {
    var mask = CIImage(cvPixelBuffer: m.pixelBuffer)
    let sx = W / mask.extent.width, sy = H / mask.extent.height
    mask = mask.transformed(by: CGAffineTransform(scaleX: sx, y: sy))
    let blur = CIFilter.gaussianBlur(); blur.inputImage = mask.clampedToExtent(); blur.radius = Float(max(1.0, W / 700.0))
    mask = blur.outputImage!.cropped(to: source.extent)

    let grad = CIFilter.radialGradient()
    grad.center = CGPoint(x: faceCX, y: faceCY + faceRect.height * 0.2)
    grad.radius0 = Float(cropH * 0.18)
    grad.radius1 = Float(cropH * 1.05)
    grad.color0 = CIColor(red: 0.90, green: 0.90, blue: 0.90)
    grad.color1 = CIColor(red: 0.62, green: 0.62, blue: 0.62)
    let backdrop = grad.outputImage!.cropped(to: source.extent)

    let blend = CIFilter.blendWithMask()
    blend.inputImage = source
    blend.backgroundImage = backdrop
    blend.maskImage = mask
    composed = blend.outputImage!.cropped(to: source.extent)
}

// ---- 4. Black-and-white grade ----
let mono = CIFilter.photoEffectMono(); mono.inputImage = composed
let cc = CIFilter.colorControls(); cc.inputImage = mono.outputImage!; cc.contrast = 1.06; cc.brightness = 0.0; cc.saturation = 0
let sharp = CIFilter.unsharpMask(); sharp.inputImage = cc.outputImage!; sharp.radius = 2.0; sharp.intensity = 0.35
let graded = sharp.outputImage!.cropped(to: crop)

// ---- 5. Output at 800x1000 and 400x500 ----
let ctx = CIContext(options: [.workingColorSpace: CGColorSpace(name: CGColorSpace.sRGB)!])
try? FileManager.default.createDirectory(at: outDir, withIntermediateDirectories: true)
for width in [800, 400] {
    let scale = CGFloat(width) / crop.width
    let lanczos = CIFilter.lanczosScaleTransform(); lanczos.inputImage = graded; lanczos.scale = Float(scale); lanczos.aspectRatio = 1
    let scaled = lanczos.outputImage!.transformed(by: CGAffineTransform(translationX: -crop.minX * scale, y: -crop.minY * scale))
    let target = CGRect(x: 0, y: 0, width: CGFloat(width), height: CGFloat(width) * 1.25).integral
    let out = outDir.appendingPathComponent("\(slug)-\(width).jpg")
    do {
        try ctx.writeJPEGRepresentation(of: scaled.cropped(to: target), to: out, colorSpace: CGColorSpace(name: CGColorSpace.sRGB)!,
                                        options: [kCGImageDestinationLossyCompressionQuality as CIImageRepresentationOption: 0.86])
    } catch { print("write failed: \(error)"); exit(3) }
}
print(String(format: "%@: source %.0fx%.0f, face %@, crop %.0fx%.0f at (%.0f,%.0f)", slug, W, H, faceFound ? "found" : "NOT found (centered fallback)", crop.width, crop.height, crop.minX, crop.minY))
