""" Tests for ParserNode interface """
from certbot_apache import assertions
from certbot_apache import augeasparser


class DualNodeBase(assertions.InterfaceAssertions):
    """ Dual parser interface for in development testing. This is used as the
    base class for dual parser interface classes. This class handles runtime
    attribute value assertions."""

    def save(self, msg):
        """ Call save for both parsers """
        self.primary.save(msg)
        self.secondary.save(msg)

    def __getattr__(self, aname):
        """ Attribute value assertion """
        firstval = getattr(self.primary, aname)
        secondval = getattr(self.secondary, aname)
        if not self.isPass(firstval, secondval):
            self.assertSimple(firstval, secondval)
        return firstval


class DualCommentNode(DualNodeBase):
    """ Dual parser implementation of CommentNode interface """

    def __init__(self, comment="", ancestor=None, filepath="", dirty=False,
                 primary=None, secondary=None):
        """ This initialization implementation allows ordinary initialization
        of CommentNode objects as well as creating a DualCommentNode object
        using precreated or fetched CommentNode objects if provided as optional
        arguments primary and secondary.
        """

        if not primary:
            self.primary = augeasparser.AugeasCommentNode(comment, ancestor,
                                                          filepath, dirty)
        else:
            self.primary = primary
        if not secondary:
            self.secondary = augeasparser.AugeasCommentNode(comment, ancestor,
                                                            filepath, dirty)
        else:
            self.secondary = secondary


class DualDirectiveNode(DualNodeBase):
    """ Dual parser implementation of DirectiveNode interface """

    def __init__(self, name="", parameters=(), ancestor=None, filepath="",
                 dirty=False, enabled=True, primary=None, secondary=None):  # pragma: no cover
        """ This initialization implementation allows ordinary initialization
        of DirectiveNode objects as well as creating a DualDirectiveNode object
        using precreated or fetched DirectiveNode objects if provided as optional
        arguments primary and secondary.
        """

        if not primary:
            self.primary = augeasparser.AugeasDirectiveNode(name, parameters,
                                                            ancestor, filepath,
                                                            dirty, enabled)
        else:
            self.primary = primary

        if not secondary:
            self.secondary = augeasparser.AugeasDirectiveNode(name, parameters,
                                                              ancestor, filepath,
                                                              dirty, enabled)
        else:
            self.secondary = secondary

    def set_parameters(self, parameters):  # pragma: no cover
        """ Sets parameters and asserts that both implementation successfully
        set the parameter sequence """

        self.primary.set_parameters(parameters)
        self.secondary.set_parameters(parameters)
        self.assertEqual(self.primary, self.secondary)


class DualBlockNode(DualNodeBase):
    """ Dual parser implementation of BlockNode interface """

    def __init__(self, name="", parameters=(), children=(), ancestor=None,
                 filepath="", dirty=False, enabled=True, primary=None,
                 secondary=None):  # pragma: no cover
        """ This initialization implementation allows ordinary initialization
        of BlockNode objects as well as creating a DualBlockNode object
        using precreated or fetched BlockNode objects if provided as optional
        arguments primary and secondary.
        """
        if not primary:
            self.primary = augeasparser.AugeasBlockNode(name, parameters, children,
                                                        ancestor, filepath, dirty,
                                                        enabled)
        else:
            self.primary = primary

        if not secondary:
            self.secondary = augeasparser.AugeasBlockNode(name, parameters, children,
                                                          ancestor, filepath, dirty,
                                                          enabled)
        else:
            self.secondary = secondary

    def add_child_block(self, name, parameters=None, position=None):  # pragma: no cover
        """ Creates a new child BlockNode, asserts that both implementations
        did it in a similar way, and returns a newly created DualBlockNode object
        encapsulating both of the newly created objects """

        primary_new = self.primary.add_child_block(name, parameters, position)
        secondary_new = self.secondary.add_child_block(name, parameters, position)
        self.assertEqual(primary_new, secondary_new)
        new_block = DualBlockNode(primary=primary_new, secondary=secondary_new)
        return new_block

    def add_child_directive(self, name, parameters=None, position=None):  # pragma: no cover
        """ Creates a new child DirectiveNode, asserts that both implementations
        did it in a similar way, and returns a newly created DualDirectiveNode
        object encapsulating both of the newly created objects """

        primary_new = self.primary.add_child_directive(name, parameters, position)
        secondary_new = self.secondary.add_child_directive(name, parameters, position)
        self.assertEqual(primary_new, secondary_new)
        new_dir = DualDirectiveNode(primary=primary_new, secondary=secondary_new)
        return new_dir

    def add_child_comment(self, comment="", position=None):  # pragma: no cover
        """ Creates a new child CommentNode, asserts that both implementations
        did it in a similar way, and returns a newly created DualCommentNode
        object encapsulating both of the newly created objects """

        primary_new = self.primary.add_child_comment(comment, position)
        secondary_new = self.secondary.add_child_comment(comment, position)
        self.assertEqual(primary_new, secondary_new)
        new_comment = DualCommentNode(primary=primary_new, secondary=secondary_new)
        return new_comment

    def find_blocks(self, name, exclude=True):  # pragma: no cover
        """
        Performs a search for BlockNodes using both implementations and
        checks the results. This is built upon the assumption that unimplemented
        find_* methods return a list with a single assertion passing object.
        After the assertion, it creates a list of newly created DualBlockNode
        instances that encapsulate the pairs of returned BlockNode objects.
        """

        primary_blocks = self.primary.find_blocks(name, exclude)
        secondary_blocks = self.secondary.find_blocks(name, exclude)

        new_blocks = list()
        # Check for assertion pass for results, as zip loses data otherwise.
        # unimplemented find_* methods should return a single object with
        # assertion pass.
        if len(primary_blocks) != len(secondary_blocks):
            if secondary_blocks:
                if self.isPass(secondary_blocks[0]):
                    for c in primary_blocks:
                        new_blocks.append(DualBlockNode(
                            primary=c, secondary=secondary_blocks[0]))
                else:
                    # Break as we got confusing results.
                    assert False
            else:
                # Break as we got confusing results.
                assert False
        else:
            for twins in zip(primary_blocks, secondary_blocks):
                self.assertEqual(twins[0], twins[1])
                new_blocks.append(DualBlockNode(primary=twins[0],
                                                secondary=twins[1]))
        return new_blocks

    def find_directives(self, name, exclude=True):  # pragma: no cover
        """
        Performs a search for DirectiveNodes using both implementations and
        checks the results. This is built upon the assumption that unimplemented
        find_* methods return a list with a single assertion passing object.
        After the assertion, it creates a list of newly created DualDirectiveNode
        instances that encapsulate the pairs of returned DirectiveNode objects.
        """
        primary_directives = self.primary.find_directives(name, exclude)
        secondary_directives = self.secondary.find_directives(name, exclude)

        new_dirs = list()
        # Check for assertion pass for results, as zip loses data otherwise.
        # unimplemented find_* methods should return a single object with
        # assertion pass.
        if len(primary_directives) != len(secondary_directives):
            if secondary_directives:
                if self.isPass(secondary_directives[0]):
                    for c in primary_directives:
                        new_dirs.append(DualDirectiveNode(
                            primary=c, secondary=secondary_directives[0]))
                else:
                    # Break as we got confusing results.
                    assert False
            else:
                # Break as we got confusing results.
                assert False
        else:
            for twins in zip(primary_directives, secondary_directives):
                self.assertEqual(twins[0], twins[1])
                new_dirs.append(DualDirectiveNode(primary=twins[0],
                                                  secondary=twins[1]))
        return new_dirs

    def find_comments(self, comment, exact=False):  # pragma: no cover
        """
        Performs a search for CommentNodes using both implementations and
        checks the results. This is built upon the assumption that unimplemented
        find_* methods return a list with a single assertion passing object.
        After the assertion, it creates a list of newly created DualCommentNode
        instances that encapsulate the pairs of returned CommentNode objects.
        """
        primary_comments = self.primary.find_comments(comment, exact)
        secondary_comments = self.secondary.find_comments(comment, exact)

        new_comments = list()
        # Check for assertion pass for results, as zip loses data otherwise.
        # unimplemented find_* methods should return a single object with
        # assertion pass.
        if len(primary_comments) != len(secondary_comments):
            if secondary_comments:
                if self.isPass(secondary_comments[0]):
                    for c in primary_comments:
                        new_comments.append(DualCommentNode(
                            primary=c, secondary=secondary_comments[0]))
                else:
                    # Break as we got confusing results.
                    assert False
            else:
                # Break as we got confusing results.
                assert False
        else:
            for twins in zip(primary_comments, secondary_comments):
                self.assertEqual(twins[0], twins[1])
                new_comments.append(DualCommentNode(primary=twins[0],
                                                      secondary=twins[1]))
        return new_comments

    def delete_child(self, child):  # pragma: no cover
        """Deletes a child from the ParserNode implementations. The actual
        ParserNode implementations are used here directly in order to be able
        to match a child to the list of children."""

        self.primary.delete_child(child.primary)
        self.secondary.delete_child(child.secondary)

    def set_parameters(self, parameters):  # pragma: no cover
        """ Sets parameters and asserts that both implementation successfully
        set the parameter sequence """

        self.primary.set_parameters(parameters)
        self.secondary.set_parameters(parameters)
        self.assertEqual(self.primary, self.secondary)

    def unsaved_files(self):  # pragma: no cover
        """ Fetches the list of unsaved file paths and asserts that the lists
        match """
        primary_files = self.primary.unsaved_files()
        secondary_files = self.secondary.unsaved_files()
        self.assertSimple(primary_files, secondary_files)

        return primary_files
