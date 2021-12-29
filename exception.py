class FinishButtonException(Exception):
    def __str__(self):
        return "終了ボタン押下"


class SkipException(Exception):
    def __str__(self, **kwargs):
        for key in kwargs:
            setattr(self, key, kwargs[key])
        return "次の処理にスキップ"
