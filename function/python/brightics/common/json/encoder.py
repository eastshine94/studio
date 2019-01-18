import json
import pickle
import numpy
<<<<<<< HEAD
import pandas as pd
from brightics.common.report import ReportBuilder


def _to_default_list(np_arr):
    return numpy.where(pd.isnull(np_arr), None, np_arr).tolist()


class DefaultEncoder(json.JSONEncoder):
    """
    DefaultEncoder is used for building viewable json string for in browser
    """
    def default(self, obj):
        # TODO add more support types
        if isinstance(obj, set):
            return list(obj)
        elif isinstance(obj, numpy.ndarray):
            return _to_default_list(obj)
        else:
            rb = ReportBuilder()
            rb.addRawTextMD(str(obj))
            return {'type': 'python object', 'report': rb.get()}


class PickleEncoder(DefaultEncoder):
    """
    PickleEncoder is used for building json string saved in redis
    """
    def encode(self, obj):
=======
from brightics.common.repr import BrtcReprBuilder


# DefaultEncoder is used for building viewable json string for in browser
class DefaultEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        elif isinstance(obj, numpy.ndarray):
            return obj.tolist()
        # TODO add more support types
        else:
        # elif hasattr(obj, '__str__'):
            rb = BrtcReprBuilder()
            rb.addRawTextMD(str(obj))
            return {'type':'python object', '_repr_brtc_':rb.get()}

     #   return 'python object'


# PickleEncoder is used for building json string saved in redis
class PickleEncoder(DefaultEncoder):

    def encode(self, obj):

>>>>>>> brtc-issue-107
        def hint_tuples(item):
            if isinstance(item, tuple):
                return {'__tuple__': [hint_tuples(e) for e in item]}
            if isinstance(item, list):
                return [hint_tuples(e) for e in item]
            if isinstance(item, dict):
                new_dict = {}
                for key in item:
                    new_dict[key] = hint_tuples(item[key])
                return new_dict
            else:
                return item

        return super(DefaultEncoder, self).encode(hint_tuples(obj))

    def default(self, o):
<<<<<<< HEAD
        # TODO add more support types
        if isinstance(o, set):
            return {'__set__': list(o)}
        elif isinstance(o, numpy.ndarray):
            return {'__numpy__': _to_default_list(o)}
        elif hasattr(o, '_repr_html_'):
            rb = ReportBuilder()
            rb.addHTML(o._repr_html_())
            return {'report': rb.get(), '__pickled__': list(pickle.dumps(o))}
        elif hasattr(o, 'savefig'):
            rb = ReportBuilder()
            rb.addPlt(o)
            return {'report': rb.get(), '__pickled__': list(pickle.dumps(o))}
        else:
            rb = ReportBuilder()
            rb.addRawTextMD(str(o))
            return {'report': rb.get(), '__pickled__': list(pickle.dumps(o))}
=======
        if isinstance(o, set):
            return {'__set__': list(o)}
        elif isinstance(o, numpy.ndarray):
            return {'__numpy__': o.tolist()}
        # TODO add more support types
        # return {'__pickled__': list(pickle.dumps(o))}
        elif hasattr(o, '_repr_html_'):
            rb = BrtcReprBuilder()
            rb.addHTML(o._repr_html_())
            return {'_repr_brtc_':rb.get(), '__pickled__': list(pickle.dumps(o))}
        elif hasattr(o, 'savefig'):
            rb = BrtcReprBuilder()
            rb.addPlt(o)
            return {'_repr_brtc_':rb.get(), '__pickled__': list(pickle.dumps(o))}
        else:
            rb = BrtcReprBuilder()
            rb.addRawTextMD(str(o))
            return {'_repr_brtc_':rb.get(), '__pickled__': list(pickle.dumps(o))}
>>>>>>> brtc-issue-107


def encode(obj, for_redis):
    if for_redis:
        return json.dumps(obj, cls=PickleEncoder)
    else:
        return json.dumps(obj, cls=DefaultEncoder)
