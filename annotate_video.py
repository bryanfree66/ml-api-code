import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="<JSON SECURITY KEY>"
from google.cloud import videointelligence

"""Detects labels given a GCS path."""
video_client = videointelligence.VideoIntelligenceServiceClient()
features = [videointelligence.Feature.LABEL_DETECTION]

mode = videointelligence.LabelDetectionMode.SHOT_AND_FRAME_MODE
config = videointelligence.LabelDetectionConfig(label_detection_mode=mode)
context = videointelligence.VideoContext(label_detection_config=config)

path='gs://ml-apis-demo/video/IMG_0220.MOV'

operation = video_client.annotate_video(
    request={"features": features, "input_uri": path, "video_context": context}
)
print("\nProcessing video for label annotations:")

result = operation.result(timeout=180)
print("\nFinished processing.")

# Process video/segment level label annotations
segment_labels = result.annotation_results[0].segment_label_annotations
for i, segment_label in enumerate(segment_labels):
    print("Video label description: {}".format(segment_label.entity.description))
    for category_entity in segment_label.category_entities:
        print(
            "\tLabel category description: {}".format(category_entity.description)
        )

    for i, segment in enumerate(segment_label.segments):
        start_time = (
            segment.segment.start_time_offset.seconds
            + segment.segment.start_time_offset.microseconds / 1e6
        )
        end_time = (
            segment.segment.end_time_offset.seconds
            + segment.segment.end_time_offset.microseconds / 1e6
        )
        positions = "{}s to {}s".format(start_time, end_time)
        confidence = segment.confidence
        print("\tSegment {}: {}".format(i, positions))
        print("\tConfidence: {}".format(confidence))
    print("\n")

# Process shot level label annotations
shot_labels = result.annotation_results[0].shot_label_annotations
for i, shot_label in enumerate(shot_labels):
    print("Shot label description: {}".format(shot_label.entity.description))
    for category_entity in shot_label.category_entities:
        print(
            "\tLabel category description: {}".format(category_entity.description)
        )

    for i, shot in enumerate(shot_label.segments):
        start_time = (
            shot.segment.start_time_offset.seconds
            + shot.segment.start_time_offset.microseconds / 1e6
        )
        end_time = (
            shot.segment.end_time_offset.seconds
            + shot.segment.end_time_offset.microseconds / 1e6
        )
        positions = "{}s to {}s".format(start_time, end_time)
        confidence = shot.confidence
        print("\tSegment {}: {}".format(i, positions))
        print("\tConfidence: {}".format(confidence))
    print("\n")

# Process frame level label annotations
frame_labels = result.annotation_results[0].frame_label_annotations
for i, frame_label in enumerate(frame_labels):
    print("Frame label description: {}".format(frame_label.entity.description))
    for category_entity in frame_label.category_entities:
        print(
            "\tLabel category description: {}".format(category_entity.description)
        )

    # Each frame_label_annotation has many frames,
    # here we print information only about the first frame.
    frame = frame_label.frames[0]
    time_offset = frame.time_offset.seconds + frame.time_offset.microseconds / 1e6
    print("\tFirst frame time offset: {}s".format(time_offset))
    print("\tFirst frame confidence: {}".format(frame.confidence))
    print("\n")