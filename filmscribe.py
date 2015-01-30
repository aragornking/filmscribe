# The MIT License (MIT)
# 
# Copyright (c) [2015] [Dobri Georgiev]
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

__author__ = 'dobri.georgiev'

from xml.sax import make_parser
from xml.sax.handler import ContentHandler
from xml.sax.handler import ErrorHandler

import sys
import traceback


class FilmscribeErrorHandler(ErrorHandler):
    def __init__(self):
        pass

    def error(self, exception):
        sys.stderr.write('ERROR {0}\n'.format(str(exception)))

    def fatalError(self, exception):
        sys.stderr.write('FATAL ERROR {0}\n'.format(str(exception)))

    def warning(self, exception):
        pass


class FilmscribeBreakException(Exception):
    pass


class FilmscribeTime(object):
    def __init__(self):
        self.__frame = None
        self.__edgecode = None
        self.__timecode = None

    @property
    def frame(self):
        return self.__frame

    @frame.setter
    def frame(self, value):
        self.__frame = value

    @property
    def edgecode(self):
        return self.__edgecode

    @edgecode.setter
    def edgecode(self, value):
        self.__edgecode = value

    @property
    def timecode(self):
        return self.__timecode

    @timecode.setter
    def timecode(self, value):
        self.__timecode = value


class FilmscribeListHead(object):
    def __init__(self):
        self.__title = None
        self.__tracks = None
        self.__event_count = 0
        self.__optical_count = 0
        self.__dupe_count = 0
        self.__edit_rate = 24
        self.__master_duration = None

    @property
    def title(self):
        return self.__title

    @title.setter
    def title(self, value):
        self.__title = value

    @property
    def tracks(self):
        return self.__tracks

    @tracks.setter
    def tracks(self, value):
        self.__tracks = value

    @property
    def event_count(self):
        return self.__event_count

    @event_count.setter
    def event_count(self, value):
        self.__event_count = value

    @property
    def optical_count(self):
        return self.__optical_count

    @optical_count.setter
    def optical_count(self, value):
        self.__optical_count = value

    @property
    def dupe_count(self):
        return self.__dupe_count

    @dupe_count.setter
    def dupe_count(self, value):
        self.__dupe_count = value

    @property
    def edit_rate(self):
        return self.__edit_rate

    @edit_rate.setter
    def edit_rate(self, value):
        self.__edit_rate = value

    @property
    def master_duration(self):
        return self.__master_duration

    @master_duration.setter
    def master_duration(self, value):
        self.__master_duration = value


class FilmscribeEvent(object):
    def __init__(self, **kwargs):
        self.__id = None
        self.__length = None
        self.__source_count = None
        self.__ref_num = None
        self.__reference = None
        self.__master = FilmscribeEventMaster()
        self.__source = FilmscribeEventSource()
        self.__type = None

        for key, value in kwargs.items():
            if key == 'num':
                self.__id = int(value)
            if key == 'length':
                self.__length = int(value)
            if key == 'sourcecount':
                self.__source_count = int(value)
            if key == 'refnum':
                self.__ref_num = int(value)
            if key == 'reference':
                self.__reference = value
            if key == 'type':
                self.__type = value

    @property
    def master(self):
        """
        :rtype: FilmscribeEventMaster
        :return: Event master
        """
        return self.__master

    @master.setter
    def master(self, value):
        self.__master = value

    @property
    def source(self):
        """
        :rtype: FilmscribeEventSource
        :return: Event source
        """
        return self.__source

    @source.setter
    def source(self, value):
        self.__source = value

    @property
    def type(self):
        """
        :rtype: str
        :return: Event type
        """
        return self.__type

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, value):
        self.__id = value

    @property
    def length(self):
        return self.__length

    @length.setter
    def length(self, value):
        self.__length = value

    @property
    def source_count(self):
        return self.__source_count

    @source_count.setter
    def source_count(self, value):
        self.__source_count = value

    @property
    def ref_num(self):
        return self.__ref_num

    @ref_num.setter
    def ref_num(self, value):
        self.__ref_num = value

    @property
    def reference(self):
        return self.__reference

    @reference.setter
    def reference(self, value):
        self.__reference = value


class FilmscribeOpticalEvent(FilmscribeEvent):
    def __init__(self, **kwargs):
        super(FilmscribeOpticalEvent, self).__init__(**kwargs)
        self.__layers = []

    @property
    def layers(self):
        """
        :rtype: list of FilmscribeOpticalLayer
        :return:
        """
        return self.__layers

    def add_layer(self, value):
        self.__layers.append(value)


class FilmscribeCutEvent(FilmscribeEvent):
    def __init__(self, **kwargs):
        super(FilmscribeCutEvent, self).__init__(**kwargs)


class FilmscribeList(object):
    def __init__(self):
        self.__head = None
        self.__events = []

    @property
    def head(self):
        """Metadata for the list.

        :rtype: FilmscribeListHead
        :return:
        """
        return self.__head

    @head.setter
    def head(self, value):
        """

        :type value: FilmscribeListHead
        :param value:
        """
        self.__head = value

    @property
    def events(self):
        """
        :rtype: list of FilmscribeEvent
        :return: All events for this Filmscribe list
        """
        return self.__events

    def add_event(self, event):
        """
        :type event: FilmscribeLocatorEvent or FilmscribeCutEvent or FilmscribeOpticalEvent
        :param event: Event to be appended to this Filmscribe list
        """
        self.__events.append(event)


class FilmscribeAssembleList(FilmscribeList):
    def __init__(self):
        super(FilmscribeAssembleList, self).__init__()


class FilmscribeOpticalList(FilmscribeList):
    def __init__(self):
        super(FilmscribeOpticalList, self).__init__()


class FilmscribeFile(object):
    def __init__(self):
        self.__version = '1.0'
        self.__date = None
        self.__assemble_lists = []
        self.__optical_lists = []

    @property
    def version(self):
        return self.__version

    @version.setter
    def version(self, value):
        self.__version = value

    @property
    def date(self):
        return self.__date

    @date.setter
    def date(self, value):
        self.__date = value

    @property
    def assemble_lists(self):
        """
        :rtype: list of FilmscribeAssembleList
        :return: Assemble lists.
        """
        return self.__assemble_lists

    @property
    def optical_lists(self):
        """
        :rtype: list of FilmscribeOpticalList
        :return:
        """
        return self.__optical_lists

    @classmethod
    def from_file(cls, filename):
        """Populate the filmscribe object from xml file.

        :type filename: str or unicode
        :param filename:
        :rtype: FilmscribeFile
        """
        filmscribe_file = cls.__new__(cls, object)
        filmscribe_file.__init__()

        if filename.endswith('.xml'):
            parser = make_parser()
            parser.setContentHandler(FilmscribeHandler(filmscribe_file))
            parser.setErrorHandler(FilmscribeErrorHandler())
            with open(filename, 'r') as infile:
                try:
                    parser.parse(infile)
                except FilmscribeBreakException:
                    pass
                except Exception as error:
                    sys.stderr.write('ERROR: Unknown error {0}\n'.format(str(error)))
                    print traceback.format_exc()

        return filmscribe_file

    def add_assemble_list(self, value):
        """Adds the given list to this FSFile object.

        :type value: FilmscribeAssembleList
        :param value: Assemble list to add
        """
        self.__assemble_lists.append(value)

    def add_optical_list(self, value):
        """Adds the given list to this FSFile object

        :type value: FilmscribeOpticalList
        :param value: Optical list to add
        """
        self.__optical_lists.append(value)


class FilmscribeEventMaster(object):
    def __init__(self):
        self.__reel = None
        self.__start = FilmscribeTime()
        self.__end = FilmscribeTime()
        self.__endout = None

    @property
    def reel(self):
        return self.__reel

    @reel.setter
    def reel(self, value):
        self.__reel = value

    @property
    def start(self):
        return self.__start

    @start.setter
    def start(self, value):
        self.__start = value

    @property
    def end(self):
        return self.__end

    @end.setter
    def end(self, value):
        self.__end = value

    @property
    def endout(self):
        return self.__endout

    @endout.setter
    def endout(self, value):
        self.__endout = value


class FilmscribeEventSource(object):
    def __init__(self):
        self.__clip_name = None
        self.__mob_id = None
        self.__start = FilmscribeTime()
        self.__end = FilmscribeTime()
        self.__endout = None
        self.__unc = None
        self.__custom = None
        self.__tape_name = None
        self.__cam_roll = None
        self.__slate = None
        self.__scene_take = None

    @property
    def clip_name(self):
        return self.__clip_name

    @clip_name.setter
    def clip_name(self, value):
        self.__clip_name = value

    @property
    def mob_id(self):
        return self.__mob_id

    @mob_id.setter
    def mob_id(self, value):
        self.__mob_id = value

    @property
    def start(self):
        return self.__start

    @start.setter
    def start(self, value):
        self.__start = value

    @property
    def end(self):
        return self.__end

    @end.setter
    def end(self, value):
        self.__end = value

    @property
    def endout(self):
        return self.__endout

    @endout.setter
    def endout(self, value):
        self.__endout = value

    @property
    def unc(self):
        return self.__unc

    @unc.setter
    def unc(self, value):
        self.__unc = value

    @property
    def custom(self):
        return self.__custom

    @custom.setter
    def custom(self, value):
        self.__custom = value

    @property
    def tape_name(self):
        return self.__tape_name

    @tape_name.setter
    def tape_name(self, value):
        self.__tape_name = value

    @property
    def cam_roll(self):
        return self.__cam_roll

    @cam_roll.setter
    def cam_roll(self, value):
        self.__cam_roll = value

    @property
    def slate(self):
        return self.__slate

    @slate.setter
    def slate(self, value):
        self.__slate = value

    @property
    def scene_take(self):
        return self.__scene_take

    @scene_take.setter
    def scene_take(self, value):
        self.__scene_take = value


class FilmscribeMotion(object):
    def __init__(self, motion_type, factor):
        self.__type = motion_type
        self.__factor = factor

    @property
    def type(self):
        return self.__type

    @property
    def factor(self):
        return self.__factor


class FilmscribeEffect(object):
    def __init__(self, effect_type):
        self.__type = effect_type

    @property
    def type(self):
        return self.__type


class FilmscribeOpticalLayer(object):
    def __init__(self, *args, **kwargs):
        self.__name = args[0] if args else None
        self.__type = None
        self.__data = None
        self.__factor = None

        for key, value in kwargs.items():
            if key == 'type':
                self.__type = value
            if key == 'factor':
                self.__factor = float(value)

        if self.__name == 'Motion':
            self.__data = FilmscribeMotion(self.__type, self.__factor)
        if self.__name == 'Effect':
            self.__data = FilmscribeEffect(self.__type)

    @property
    def type(self):
        return self.__type

    @property
    def name(self):
        return self.__name

    @property
    def data(self):
        return self.__data


class FilmscribeLocatorEvent(FilmscribeEvent):
    def __init__(self, **kwargs):
        super(FilmscribeLocatorEvent, self).__init__(**kwargs)
        self.__color = None
        self.__text = ''

    @property
    def color(self):
        return self.__color

    @color.setter
    def color(self, value):
        self.__color = value

    @property
    def text(self):
        return self.__text

    @text.setter
    def text(self, value):
        self.__text = value


class FilmscribeHandler(ContentHandler):
    def __init__(self, filmscribe_file):
        """

        :type filmscribe_file: FilmscribeFile
        :param filmscribe_file:
        """
        ContentHandler.__init__(self)
        self.__filmscribe_file = filmscribe_file
        self.__current_list = None
        self.__xpath = []
        self.__element_text = ''

    def get_parent(self):
        if len(self.__xpath) > 1:
            return self.__xpath[-2]
        return ''

    def is_descendant_of(self, name):
        return name in self.__xpath

    def handle_start(self, root, name):
        if name == 'Frame':
            root.start.frame = int(self.__element_text)
        if name == 'Timecode':
            root.start.timecode = self.__element_text
        if name == 'Edgecode':
            root.start.edgecode = self.__element_text

    def handle_end(self, root, name):
        if name == 'Frame':
            root.end.frame = int(self.__element_text)
        if name == 'Timecode':
            root.end.timecode = self.__element_text
        if name == 'Edgecode':
            root.end.edgecode = self.__element_text

    def startElement(self, name, attrs):
        self.__element_text = ''
        self.__xpath.append(name)

        if name == 'FilmScribeFile':
            self.__filmscribe_file.date = attrs.get('Date')
            self.__filmscribe_file.version = attrs.get('Version')

        if name == 'AssembleList':
            self.__current_list = FilmscribeAssembleList()

        if name == 'OpticalList':
            self.__current_list = FilmscribeOpticalList()

        if name == 'ListHead':
            self.__current_list.head = FilmscribeListHead()

        if name == 'MasterDuration':
            self.__current_list.head.master_duration = FilmscribeTime()

        if name == 'Event':
            if attrs.get('Type') == 'Cut':
                kwargs = dict((k.lower(), v) for k, v in attrs.items())
                e = FilmscribeCutEvent(**kwargs)
                self.__current_list.add_event(e)
            if attrs.get('Type') == 'Optical':
                kwargs = dict((k.lower(), v) for k, v in attrs.items())
                e = FilmscribeOpticalEvent(**kwargs)
                self.__current_list.add_event(e)

        if name == 'Comment' and self.get_parent() == 'Events':
            if attrs.get('Type') == 'Locator':
                kwargs = dict((k.lower(), v) for k, v in attrs.items())
                e = FilmscribeLocatorEvent(**kwargs)
                self.__current_list.add_event(e)

        if self.get_parent() == 'Layer' and self.is_descendant_of('Event'):
            e = self.__current_list.events[-1]
            if isinstance(e, FilmscribeOpticalEvent) and isinstance(self.__current_list, FilmscribeOpticalList):
                kwargs = dict((k.lower(), v) for k, v in attrs.items())
                e.add_layer(FilmscribeOpticalLayer(name, **kwargs))

    def endElement(self, name):
        if name == 'FilmScribeFile':
            raise FilmscribeBreakException

        if name == 'AssembleList':
            self.__filmscribe_file.add_assemble_list(self.__current_list)

        if name == 'OpticalList':
            self.__filmscribe_file.add_optical_list(self.__current_list)

        if name == 'Title':
            self.__current_list.head.title = self.__element_text

        if name == 'Tracks':
            self.__current_list.head.tracks = self.__element_text

        if name == 'EventCount':
            self.__current_list.head.event_count = self.__element_text

        if name == 'EditRate':
            self.__current_list.head.edit_rate = float(self.__element_text)

        if name == 'OpticalCount':
            self.__current_list.head.optical_count = self.__element_text

        if name == 'FrameCount' and self.get_parent() == 'MasterDuration':
            self.__current_list.head.master_duration.frame = int(self.__element_text)

        if name == 'Edgecode' and self.get_parent() == 'MasterDuration':
            self.__current_list.head.master_duration.edgecode = self.__element_text

        if name == 'Timecode' and self.get_parent() == 'MasterDuration':
            self.__current_list.head.master_duration.timecode = self.__element_text

        # Master
        # # Start
        if self.get_parent() == 'Start' and self.is_descendant_of('Event') and self.is_descendant_of('Master'):
            e = self.__current_list.events[-1]
            if isinstance(self.__current_list, (FilmscribeAssembleList, FilmscribeOpticalList)):
                self.handle_start(e.master, name)

        # # End
        if self.get_parent() == 'End' and self.is_descendant_of('Event') and self.is_descendant_of('Master'):
            e = self.__current_list.events[-1]
            if isinstance(self.__current_list, (FilmscribeAssembleList, FilmscribeOpticalList)):
                self.handle_end(e.master, name)

        # # Endout
        if self.get_parent() == 'EndOut' and self.is_descendant_of('Event') and self.is_descendant_of('Master'):
            e = self.__current_list.events[-1]
            if isinstance(self.__current_list, (FilmscribeAssembleList, FilmscribeOpticalList)):
                if name == 'Timecode':
                    e.master.endout = self.__element_text

        # Source
        # # ClipName
        if name == 'ClipName' and self.is_descendant_of('Event') and self.get_parent() == 'Source':
            e = self.__current_list.events[-1]
            if isinstance(self.__current_list, (FilmscribeAssembleList, FilmscribeOpticalList)):
                e.source.clip_name = self.__element_text

        # # MobID
        if name == 'MobID' and self.is_descendant_of('Event') and self.get_parent() == 'Source':
            e = self.__current_list.events[-1]
            if isinstance(self.__current_list, (FilmscribeAssembleList, FilmscribeOpticalList)):
                e.source.mob_id = self.__element_text

        # # Start
        if self.get_parent() == 'Start' and self.is_descendant_of('Event') and self.is_descendant_of('Source'):
            e = self.__current_list.events[-1]
            if isinstance(self.__current_list, (FilmscribeAssembleList, FilmscribeOpticalList)):
                self.handle_start(e.source, name)

        ## End
        if self.get_parent() == 'End' and self.is_descendant_of('Event') and self.is_descendant_of('Source'):
            e = self.__current_list.events[-1]
            if isinstance(self.__current_list, (FilmscribeAssembleList, FilmscribeOpticalList)):
                self.handle_end(e.source, name)

        ## Endout
        if self.get_parent() == 'EndOut' and self.is_descendant_of('Event') and self.is_descendant_of('Source'):
            e = self.__current_list.events[-1]
            if isinstance(self.__current_list, (FilmscribeAssembleList, FilmscribeOpticalList)):
                if name == 'Timecode':
                    e.source.endout = self.__element_text

        ## UNC
        if name == 'UNC' and self.is_descendant_of('Event') and self.get_parent() == 'Source':
            e = self.__current_list.events[-1]
            if isinstance(self.__current_list, (FilmscribeAssembleList, FilmscribeOpticalList)):
                e.source.unc = self.__element_text

        ## Custom
        if name == 'Custom' and self.is_descendant_of('Event') and self.get_parent() == 'Source':
            e = self.__current_list.events[-1]
            if isinstance(self.__current_list, (FilmscribeAssembleList, FilmscribeOpticalList)):
                e.source.custom = self.__element_text

        ## TypeName
        if name == 'TapeName' and self.is_descendant_of('Event') and self.get_parent() == 'Source':
            e = self.__current_list.events[-1]
            if isinstance(self.__current_list, (FilmscribeAssembleList, FilmscribeOpticalList)):
                e.source.tape_name = self.__element_text

        ## CamRoll
        if name == 'CamRoll' and self.is_descendant_of('Event') and self.get_parent() == 'Source':
            e = self.__current_list.events[-1]
            if isinstance(self.__current_list, (FilmscribeAssembleList, FilmscribeOpticalList)):
                e.source.cam_roll = self.__element_text

        ## SceneTake
        if name == 'SceneTake' and self.is_descendant_of('Event') and self.get_parent() == 'Source':
            e = self.__current_list.events[-1]
            if isinstance(self.__current_list, (FilmscribeAssembleList, FilmscribeOpticalList)):
                e.source.scene_take = self.__element_text

        ## Slate
        if name == 'Slate' and self.is_descendant_of('Event') and self.get_parent() == 'Source':
            e = self.__current_list.events[-1]
            if isinstance(self.__current_list, (FilmscribeAssembleList, FilmscribeOpticalList)):
                e.source.slate = self.__element_text

        # Comment
        ## Master
        if self.get_parent() == 'Master' and self.is_descendant_of('Comment'):
            e = self.__current_list.events[-1]
            if isinstance(self.__current_list, FilmscribeAssembleList):
                self.handle_start(e.master, name)

        ## Source
        if self.get_parent() == 'Source' and self.is_descendant_of('Comment'):
            e = self.__current_list.events[-1]
            if isinstance(self.__current_list, FilmscribeAssembleList):
                if name == 'ClipName':
                    e.source.clip_name = self.__element_text

        ## Color
        if name == 'Color' and self.get_parent() == 'Comment':
            e = self.__current_list.events[-1]
            if isinstance(self.__current_list, FilmscribeAssembleList):
                e.color = self.__element_text

        ## Text
        if name == 'Text' and self.get_parent() == 'Comment':
            e = self.__current_list.events[-1]
            if isinstance(self.__current_list, FilmscribeAssembleList):
                e.text = self.__element_text

        self.__xpath.pop()

    def characters(self, content):
        self.__element_text += content


def main():
    filename = 'testdata/filmscribe.xml'
    filmscribe = FilmscribeFile.from_file(filename)
    for alist in filmscribe.assemble_lists:
        print 'AssembleList - {title} - {track} ( {edit_rate}/{duration} )'.format(
            title=alist.head.title,
            track=alist.head.tracks,
            edit_rate=alist.head.edit_rate,
            duration=alist.head.master_duration.frame)

        for event in alist.events:
            if isinstance(event, FilmscribeEvent):
                print '#{id:<3} SOURCE {v} {type:>8} {tname:>24} {sfin:>8}{sfout:>8} MASTER {fin:>4}/{fout:>4}'.format(
                    id=event.id,
                    tname=event.source.clip_name,
                    sfin=event.source.start.frame,
                    sfout=event.source.end.frame,
                    fin=event.master.start.frame,
                    fout=event.master.end.frame,
                    v=alist.head.tracks,
                    type=event.type)
            if isinstance(event, FilmscribeLocatorEvent):
                print '\tLocator {text} {color} {mstart:>8} {mend:>8}'.format(
                    text=event.text,
                    color=event.color,
                    mstart=event.master.start.frame,
                    mend=event.source.clip_name
                )

    for optical in filmscribe.optical_lists:
        print 'OpticalList - {title} - {track} ( {edit_rate}/{duration} )'.format(
            title=alist.head.title,
            track=alist.head.tracks,
            edit_rate=alist.head.edit_rate,
            duration=alist.head.master_duration.frame)

        for event in optical.events:
            print '#{id:<3} SOURCE {v} {type:>8} {layers}'.format(
                id=event.id,
                v=alist.head.tracks,
                type=event.type,
                layers=','.join([layer.name for layer in event.layers]))


if __name__ == '__main__':
    main()
