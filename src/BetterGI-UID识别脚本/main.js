(async function () {
    // 1. 截取游戏画面
    const capture = captureGameRegion();

    // 2. 裁剪 UID 区域（右下角那行数字的位置）
    const uidRegion = capture.DeriveCrop(1630, 1040, 270, 40);

    // 3. 对这个区域做 OCR 文字识别
    const ocrRo = RecognitionObject.Ocr(0, 0, uidRegion.width, uidRegion.height);

    // 4. 执行识别
    const result = uidRegion.find(ocrRo);

    if (result.isExist()) {
        // UID 是 9 位纯数字，用正则提取
        const uidMatch = result.text.match(/\b\d{9}\b/);
        if (uidMatch) {
            log.info("========== UID 识别成功 ==========");
            log.info(uidMatch[0]);
        } else {
            log.info("OCR 识别到的文字: \"" + result.text + "\"，但没找到 9 位数字，可能是裁剪区域不准");
        }
    } else {
        log.info("UID 区域没识别到任何文字，请确认游戏画面正常显示");
    }

    // 5. 释放资源（很重要，不然内存会越占越多）
    uidRegion.Dispose();
    capture.Dispose();
})();