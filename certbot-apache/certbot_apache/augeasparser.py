""" Tests for ParserNode interface """
from certbot_apache import interfaces


class AugeasParserNode(interfaces.ParserNode):
    """ Augeas implementation of ParserNode interface """

    def __init__(self, ancestor=None, filepath="", dirty=False):
        self.ancestor = ancestor
        # self.filepath = filepath
        self.filepath = "CERTBOT_PASS_ASSERT"
        self.dirty = dirty

    def save(self, msg):  # pragma: no cover
        pass


class AugeasCommentNode(AugeasParserNode):
    """ Augeas implementation of CommentNode interface """

    def __init__(self, comment, ancestor, filepath, dirty=False):
        super(AugeasCommentNode, self).__init__(ancestor, filepath, dirty=)
        self.comment = comment


class AugeasDirectiveNode(AugeasParserNode):
    """ Augeas implementation of DirectiveNode interface """

    def __init__(self, name, parameters=(), ancestor=None, filepath="",
                 dirty=False, enabled=True):  # pragma: no cover
        super(AugeasDirectiveNode, self).__init__(ancestor, filepath, dirty)
        self.name = name
        self.parameters = parameters
        self.enabled = enabled

    def set_parameters(self, parameters):  # pragma: no cover
        self.parameters = tuple("CERTBOT_PASS_ASSERT")


class AugeasBlockNode(AugeasParserNode):
    """ Augeas implementation of BlockNode interface """

    def __init__(self, name="", parameters=(), children=(), ancestor=None,
                 filepath="", dirty=False, enabled=True):  # pragma: no cover
        super(AugeasBlockNode, self).__init__(ancestor, filepath, dirty)
        self.name = name
        self.parameters = parameters
        self.children = children
        self.enabled = enabled

    def add_child_block(self, name, parameters=None, position=None):  # pragma: no cover
        new_block = AugeasBlockNode("CERTBOT_PASS_ASSERT", ancestor=self)
        self.children += (new_block,)
        return new_block

    def add_child_directive(self, name, parameters=None, position=None):  # pragma: no cover
        new_dir = AugeasDirectiveNode("CERTBOT_PASS_ASSERT", ancestor=self)
        self.children += (new_dir,)
        return new_dir

    def add_child_comment(self, comment="", position=None):  # pragma: no cover
        new_comment = AugeasCommentNode("CERTBOT_PASS_ASSERT", ancestor=self)
        self.children += (new_comment,)
        return new_comment

    def find_blocks(self, name, exclude=True):  # pragma: no cover
        return [AugeasBlockNode("CERTBOT_PASS_ASSERT", ancestor=self)]

    def find_directives(self, name, exclude=True):  # pragma: no cover
        return [AugeasDirectiveNode("CERTBOT_PASS_ASSERT", ancestor=self)]

    def find_comments(self, comment, exact=False):  # pragma: no cover
        return [AugeasCommentNode("CERTBOT_PASS_ASSERT", ancestor=self)]

    def delete_child(self, child):  # pragma: no cover
        pass

    def set_parameters(self, parameters):  # pragma: no cover
        self.parameters = tuple("CERTBOT_PASS_ASSERT")

    def unsaved_files(self):  # pragma: no cover
        return ["CERTBOT_PASS_ASSERT"]
