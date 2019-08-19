from certbot_apache import interfaces


class InterfaceAssertions(object):
    """ Class for handling assertions of results from two ParserNode
    implementations using a dual interface. """

    def assertEqual(self, first, second):
        """ Equality assertion """

        if isinstance(first, interfaces.CommentNode):
            self._assertEqualComment(first, second)
        elif isinstance(first, interfaces.DirectiveNode):
            self._assertEqualDirective(first, second)
        elif isinstance(first, interfaces.BlockNode):
            self._assertEqualBlock(first, second)

        # Skip tests if filepath includes the pass value. This is done
        # because filepath is variable of the base ParserNode interface, and
        # unless the implementation is actually done, we cannot assume getting
        # correct results from boolean assertion for dirty
        if not self.isPass(first.filepath, second.filepath):
            assert first.dirty == second.dirty
            # We might want to disable this later if testing with two separate
            # (but identical) directory structures.
            assert first.filepath == second.filepath

    def _assertEqualComment(self, first, second):
        """ Equality assertion for CommentNode """

        # first was checked in the assertEqual method
        assert isinstance(second, interfaces.CommentNode)

        if not self.isPass(first.comment, second.comment):
            assert first.comment == second.comment

    def _assertEqualDirective(self, first, second):
        """ Equality assertion for DirectiveNode """

        # first was checked in the assertEqual method
        assert isinstance(second, interfaces.DirectiveNode)
        # Enabled value cannot be asserted, because Augeas implementation
        # is unable to figure that out.
        # assert first.enabled == second.enabled
        if not self.isPass(first.name, second.name):
            assert first.name == second.name
        if not self.isPass(first.parameters, second.parameters):
            assert first.parameters == second.parameters

    def _assertEqualBlock(self, first, second):
        """ Equality assertion for BlockNode """

        # first was checked in the assertEqual method
        assert isinstance(second, interfaces.BlockNode)
        # Enabled value cannot be asserted, because Augeas implementation
        # is unable to figure that out.
        # assert first.enabled == second.enabled
        if not self.isPass(first.name, second.name):
            assert first.name == second.name
        if not self.isPass(first.parameters, second.parameters):
            assert first.parameters == second.parameters
        # Children cannot be asserted, because Augeas implementation will not
        # prepopulate the sequence of children.
        # assert len(first.children) == len(second.children)

    def isPass(self, first, second):
        """ Checks if either first or second holds the assertion pass value """

        if isinstance(first, tuple) or isinstance(first, list):
            if "CERTBOT_PASS_ASSERT" in first:
                return True
        if isinstance(second, tuple) or isinstance(second, list):
            if "CERTBOT_PASS_ASSERT" in second:
                return True
        if "CERTBOT_PASS_ASSERT" in [first, second]:
            return True
        return False

    def assertSimple(self, first, second):
        """ Simple assertion """
        if not self.isPass(first, second):
            assert first == second

    def assertSimpleList(self, first, second):
        """ Simple assertion that lists contain the same objects. This needs to
        be used when there's uncertainty about the ordering of the list. """

        if not self.isPass(first, second):
            if first:
                for f in first:
                    assert f in second
