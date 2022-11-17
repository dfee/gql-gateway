from gateway.client.page import (
    AfterLimitOffset,
    BeforeLimitOffset,
    LimitOffsetPageInfoMetadata,
)


class TestAfterLimitOffset:
    def test_from_0_returning_all(self):
        _offset = 0
        _first = 2

        lo = AfterLimitOffset(_after=_offset, _first=_first)
        assert lo.limit == 3
        assert lo.offset == 0
        assert lo.to_page_info_metadata(
            list(range(_first))
        ) == LimitOffsetPageInfoMetadata(
            end_offset=None,
            first=None,
            start_offset=None,
            last=None,
        )

    def test_from_0_returning_all_plus_1(self):
        _offset = 0
        _first = 2

        lo = AfterLimitOffset(_after=_offset, _first=_first)
        assert lo.limit == 3
        assert lo.offset == 0
        assert lo.to_page_info_metadata(
            list(range(lo.limit))
        ) == LimitOffsetPageInfoMetadata(
            end_offset=2,
            first=2,
            start_offset=None,
            last=None,
        )

    def test_from_1_returning_all_plus_1(self):
        _offset = 1
        _first = 2

        lo = AfterLimitOffset(_after=_offset, _first=_first)
        assert lo.limit == 3
        assert lo.offset == 1
        assert lo.to_page_info_metadata(
            list(range(_first))
        ) == LimitOffsetPageInfoMetadata(
            end_offset=None,
            start_offset=2,
            first=None,
            last=1,
        )


class TestBeforeLimitOffset:
    def test_from_1_returning_neg_indices(self):
        _offset = 1
        _last = 2

        lo = BeforeLimitOffset(_before=_offset, _last=_last)
        assert lo.limit == 1
        assert lo.offset == 0
        assert lo.to_page_info_metadata(
            list(range(lo._last))
        ) == LimitOffsetPageInfoMetadata(
            end_offset=0,
            first=2,
            start_offset=None,
            last=None,
        )

    def test_from_2_returning_all(self):
        _offset = 2
        _last = 2

        lo = BeforeLimitOffset(_before=_offset, _last=_last)
        assert lo.limit == 2
        assert lo.offset == 0
        assert lo.to_page_info_metadata(
            list(range(lo._last))
        ) == LimitOffsetPageInfoMetadata(
            end_offset=1,
            first=2,
            start_offset=None,
            last=None,
        )

    def test_from_3_returning_all_plus_1(self):
        _offset = 3
        _last = 2

        lo = BeforeLimitOffset(_before=_offset, _last=_last)
        assert lo.limit == 2
        assert lo.offset == 0
        assert lo.to_page_info_metadata(
            list(range(lo._last))
        ) == LimitOffsetPageInfoMetadata(
            end_offset=2,
            first=2,
            start_offset=1,
            last=1,
        )

    def test_from_10_returning_all_plus_1(self):
        _offset = 10
        _last = 2

        lo = BeforeLimitOffset(_before=_offset, _last=_last)
        assert lo.limit == 2
        assert lo.offset == 7
        assert lo.to_page_info_metadata(
            list(range(lo._last))
        ) == LimitOffsetPageInfoMetadata(
            end_offset=9,
            first=2,
            start_offset=8,
            last=2,
        )
