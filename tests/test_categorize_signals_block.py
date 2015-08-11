from collections import defaultdict
import re
from nio.common.signal.base import Signal
from nio.util.support.block_test_case import NIOBlockTestCase
from ..categorize_signals_block import CategorizeSignals


class TestCategorizeSignals(NIOBlockTestCase):

    def setUp(self):
        super().setUp()
        # This will keep a list of signals notified for each output
        self.last_notified = defaultdict(list)
        self._categories_config = [
            {
                'category': 'cat1',
                'patterns': ['pattern1a', 'pattern1b']
            },
            {
                'category': 'cat2',
                'patterns': ['pattern2a', 'pattern2b']
            }
        ]

    def signals_notified(self, signals, output_id='default'):
        self.last_notified[output_id].extend(signals)

    def test_configure_block(self):
        blk = CategorizeSignals()
        self.configure_block(blk, {'categories': self._categories_config})
        self.assertEqual(blk._compiled, [
            ('cat1', re.compile('pattern1a|pattern1b')),
            ('cat2', re.compile('pattern2a|pattern2b'))
        ])

    def test_text_matching(self):
        blk = CategorizeSignals()
        self.configure_block(blk, {
            'string': '{{ $text }}',
            'categories': self._categories_config
        })
        blk.start()
        blk.process_signals([
            Signal({'text': 'pattern1a'}),
            Signal({'text': 'pattern2a'}),
            Signal({'text': 'pattern3a'}),
            Signal({'text': 'pattern1b and pattern2b'})
        ])
        blk.stop()
        self.assert_num_signals_notified(4)
        self.assertDictEqual(self.last_notified['default'][0].to_dict(), {
            'text': 'pattern1a',
            'cats': ['cat1']
        })
        self.assertDictEqual(self.last_notified['default'][1].to_dict(), {
            'text': 'pattern2a',
            'cats': ['cat2']
        })
        self.assertDictEqual(self.last_notified['default'][2].to_dict(), {
            'text': 'pattern3a',
            'cats': []
        })
        self.assertDictEqual(self.last_notified['default'][3].to_dict(), {
            'text': 'pattern1b and pattern2b',
            'cats': ['cat1', 'cat2']
        })

    def test_invalid_match_string(self):
        blk = CategorizeSignals()
        self.configure_block(blk, {
            'string': '{{ text }}',
            'categories': self._categories_config
        })
        blk.start()
        blk.process_signals([
            Signal({'text': 'pattern1a'})
        ])
        blk.stop()
        self.assert_num_signals_notified(1)
