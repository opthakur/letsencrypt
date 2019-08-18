from certbot_apache import interfaces


class InterfaceAssertions(object):
    """ Mixin class for handling assertions of results from two ParserNode
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
        if not self._isPass(first.filepath, second.filepath):
            assert first.dirty == second.dirty
            # We might want to disable this later if testing with two separate
            # (but identical) directory structures.
            assert first.filepath == second.filepath

    def _assertEqualComment(self, first, second):
        """ Equality assertion for CommentNode """

        # first was checked in the assertEqual method
        assert isinstance(second, interfaces.CommentNode)
        assert first.comment == second.comment

    def _assertEqualDirective(self, first, second):
        """ Equality assertion for DirectiveNode """

        # first was checked in the assertEqual method
        assert isinstance(second, interfaces.DirectiveNode)
        assert first.enabled == second.enabled
        assert first.name == second.name
        assert first.parameters == second.parameters

    def _assertEqualBlock(self, first, second):
        """ Equality assertion for BlockNode """

        # first was checked in the assertEqual method
        assert isinstance(second, interfaces.BlockNode)
        assert first.enabled == second.enbled
        assert first.name == second.name
        assert first.parameters == second.parameters
        assert len(first.children) == len(second.children)

    def _isPass(self, first, second):
        """ Checks if either first or second holds the assertion pass value """

        if instanceof(tuple, first) or instanceof(list, first):
            if "CERTBOT_PASS_ASSERT" in first:
                return True
        if instanceof(tuple, second) or instanceof(list, second):
            if "CERTBOT_PASS_ASSERT" in second:
                return True
        if "CERTBOT_PASS_ASSERT" in [first, second]:
            return True
        return False

