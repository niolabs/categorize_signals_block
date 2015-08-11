import re
from nio.common.block.base import Block
from nio.common.discovery import Discoverable, DiscoverableType
from nio.metadata.properties import StringProperty, ExpressionProperty, \
    VersionProperty, ObjectProperty, PropertyHolder, ListProperty


class Category(PropertyHolder):
    category = StringProperty(default='cat', title='Category to Assign')
    patterns = ListProperty(str, title='Regular Expression Patterns')


@Discoverable(DiscoverableType.block)
class CategorizeSignals(Block):

    """Assign categories to posts based on a regular expression search"""

    version = VersionProperty('0.1.0')
    attr = StringProperty(title='Attribute to set', default='cats')
    string = ExpressionProperty(title="Match String",
                                default='', attr_default=Exception)
    categories = ListProperty(Category, title='Categories')

    def __init__(self):
        super().__init__()
        self._compiled = None

    def configure(self, context):
        super().configure(context)
        self._compiled = self._compile_patterns()

    def process_signals(self, signals, input_id='default'):
        for signal in signals:
            self._process_signal(signal)
        self.notify_signals(signals, output_id='default')

    def _compile_patterns(self):
        """Build and compile regex patterns.

        Return:
            list of tuples ((category, compiled_regex_pattern))

        """
        return_list = []
        for category in self.categories:
            return_list.append((category.category,
                                re.compile('|'.join(category.patterns))))
        return return_list

    def _process_signal(self, signal):
        # Prepare signal by checking the category attribute and Match String
        if not hasattr(signal, self.attr):
            setattr(signal, self.attr, [])
        if not isinstance(getattr(signal, self.attr), list):
            self._logger.exception(
                'Category attribute needs to be a list: {}'.format(self.attr))
            return
        try:
            match_string = str(self.string(signal))
        except:
            self._logger.exception(
                'Match String needs to evaluate to a string')
            return
        # Check if regex matches and append category to attr if match
        for category in self._compiled:
            match = category[1].search(match_string)
            if match is not None:
                getattr(signal, self.attr).append(category[0])
