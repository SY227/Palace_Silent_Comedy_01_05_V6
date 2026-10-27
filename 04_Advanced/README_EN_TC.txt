OPTIONAL: PREPARE A DOCUMENTED GROK IMAGINE 1.5 API REQUEST
選用：準備符合官方文件的 Grok Imagine 1.5 API 請求

This is an optional technical route, not required for normal app use. The supplied Python script only creates a local JSON file. It does not submit a video request, need a key, or spend credits. A separate authenticated API submission is required to generate video.
本方式供需要API控制時使用，一般介面操作不必用。本Python程式只在本機建立JSON，不提交生成、不需要金鑰、也不花額度。真正生成需要另外經已驗證身份的API提交。

From the extracted package root / 在解壓後的素材包根目錄：
python3 04_Advanced/build_grok_request.py --episode EP04 --mode anchors --language EN --out EP04_request.json

Choose references for eight chronological appearance/story references; choose anchors for first+last+four interior pins, plus two supplementary references. Both modes use all eight PNG assets and request one complete15-second9:16 film. The generated JSON embeds the PNGs as data URIs, so the file is large. Never paste that JSON into a normal chat prompt box.
references模式使用8張按順序的參考圖；anchors模式使用首尾、4個中間鎖定點，以及2張補充參考。兩種都用齊8張PNG並要求一支完整15秒9:16影片。JSON內嵌PNG資料，因此檔案較大，不要貼進一般聊天提示詞輸入框。

Endpoint documented by xAI / 官方文件中的端點：POST https://api.x.ai/v1/videos/generations
Model / 模型：grok-imagine-video-1.5
Resolution / 解析度：720p reference mode
Inputs / 素材：F01 first; F03@3s; F04@5s; F05@7s; F07@11.5s; F08 last; F02/F06 supplementary.

The script was checked offline for asset counts, required files and request structure. No live API request was run. Actual model output still needs the motion checks in00_Series.
程式僅離線檢查素材數目、必要檔案與請求結構，未呼叫實際API。生成結果仍需按00_Series的動態檢查表驗收。

Capability source, checked26Oct2026 / 功能來源，核對日期2026年10月26日：
https://docs.x.ai/developers/model-capabilities/video/reference-to-video
https://docs.x.ai/developers/model-capabilities/video/image-to-video

V6 audio policy: this builder inserts the updated silent-visual prompt. It does not invent or send an audio=false parameter. If the service returns audio anyway, remove that full track in editing; separately verify mouths stay closed. Add jazz and clean object Foley in post only.
V6音訊政策：程式嵌入新版無聲畫面提示詞，不杜撰或傳送audio=false參數。服務若仍回傳音訊，剪輯時完整移除原音軌，並另行確認嘴唇保持閉合；爵士及乾淨物件音效只在後期加入。


Preserve existing glass transparency and reflection geometry. Do not invent reflected faces, duplicate people or impossible mirrored rooms. Keep incidental reflections simple and stable.
保留原有玻璃透明度與反射空間，不新增反射人臉、重複人物或不可能的鏡中房間；非故事重點的反射保持簡單穩定。
Generate no audio; no dialogue, narration or human utterances. Do not supply voice references or reference_audios. Jazz and clean object Foley are added separately in post after discarding source audio.
不生成音訊、對白、旁白或任何人聲。不提供聲音參考或reference_audios。先丟棄原音軌，再於後期另加爵士及乾淨物件音效。

Optional offline export helper: 04_Advanced/export_without_source_audio.py. It removes the original audio completely and can accept a separately supplied music track; this never fixes visible talking. Verify the actual final export is 15 seconds and 9:16. Do not stretch faces or blindly crop key action to force the ratio.
選用離線輸出工具：04_Advanced/export_without_source_audio.py。完整移除原音軌，可另用獨立提供的配樂；它不能修好可見說話動作。實際輸出須檢查15秒及9:16；不要拉伸臉部或盲目裁掉關鍵動作來硬湊比例。

EXPORT WITHOUT GENERATED AUDIO / 排除生成原音軌
Requires Python 3, ffmpeg and ffprobe on your computer.
電腦需已安裝Python 3、ffmpeg及ffprobe。

Silent review export / 無音軌檢查版：
python3 04_Advanced/export_without_source_audio.py "accepted_visual.mp4" "silent_review.mp4"

Final export using ONLY your separately approved instrumental mix / 最終只採用另行確認的純演奏混音：
python3 04_Advanced/export_without_source_audio.py "accepted_visual.mp4" "final_with_jazz.mp4" --music "approved_jazz_and_foley.wav"

The optional replacement file can contain instrumental jazz and clean object Foley. Review it yourself for zero human voices. The script never maps the generated clip's source audio. It preserves the picture without cropping or stretching and reports whether the source dimensions are exactly 9:16. It does not generate music, repair lips/reflections, or automatically fix the aspect ratio. No music file is included in this kit.
替換檔可包含純演奏爵士及乾淨物件音效，須自行確認完全沒有人聲。程式不會映射生成影片的原音軌，保留原畫面而不裁切、不拉伸，並回報原尺寸是否正好9:16。程式不生成音樂、不修補嘴形或反射，也不自動修正比例；本包未附音樂檔。
