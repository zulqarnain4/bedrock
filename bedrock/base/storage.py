from pipeline.storage import PipelineMixin
from whitenoise.django import ManifestStaticFilesStorage


class ManifestPipelineStorage(PipelineMixin, ManifestStaticFilesStorage):
    pass
