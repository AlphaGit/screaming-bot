import unittest
from functions import *

class TestCleanup(unittest.TestCase):
    def test_html_tags(self):
        self.assertEqual('internal text', clean_up('<a href="something">internal text</a>'))
        self.assertEqual('Togetherness', clean_up('<a href="something">Together</a>ness'))
        self.assertEqual('Some\ntext', clean_up('<p>Some</p><p>text</p>'))
        self.assertEqual('Togetherness', clean_up('<b>Together</b>ness'))
        self.assertEqual('Some\ntext', clean_up('<blockquote>Some</blockquote>text'))
        self.assertEqual('Some\ntext', clean_up('<h1>Some</h1>text'))
        self.assertEqual('Some\ntext', clean_up('Some<br/><br/><br/>text'))
        self.assertEqual('Italics', clean_up('Ita<i>lics</i>'))
        self.assertEqual('Some\ntext', clean_up('<sub>Some</sub>text'))
        self.assertEqual('Some\ntext', clean_up('Some<hr>text'))
        self.assertEqual('Some\ntext', clean_up('<div>Some</div>text'))
        self.assertEqual('Some\ntext', clean_up('Some<iframe width="540" height="405" id="youtube_iframe" src="https://www.youtube.com/embed/j7kLNJWTDYA?feature=oembed&enablejsapi=1&origin=https://safe.txmblr.com&wmode=opaque" frameborder="0" allowfullscreen=""></iframe>text'))
        self.assertEqual('Some text', clean_up('Some <strong>text</strong>'))
        self.assertEqual('Some\ntext', clean_up('<sup>Some</sup>text'))
        self.assertEqual('yeah', clean_up('<span class="npf_color_joey">yeah</span>'))
        self.assertEqual('Someone', clean_up('Some<em>one</em>'))
        self.assertEqual('Someone', clean_up('Some<small>one</small>'))
        self.assertEqual('Item 1\nItem 2', clean_up('<ul><li>Item 1</li><li>Item 2</li></ul>'))
        self.assertEqual('Item 1\nItem 2', clean_up('<ol><li>Item 1</li><li>Item 2</li></ol>'))
        self.assertEqual('with everyone', clean_up('<strike>with every</strike>one'))
        self.assertEqual('Test1\nTest2', clean_up('Test1<video controls="controls" autoplay="autoplay" muted="muted" poster="https://78.media.tumblr.com/something.jpg"><source src="https://vt.media.tumblr.com/something.mp4" type="video/mp4"></source></video>Test2'))

    def test_username_removal(self):
        self.assertEqual('hello', clean_up('<p><a href="http://somelink" class="tumblr_blog">balamist</a>:</p><blockquote>\n<p><b>hello</b></p></blockquote>'))
        self.assertEqual('', clean_up('<p><a class="tumblr_blog" href="http://lohaanda.tumblr.com/post/113527994194">lohaanda</a>:</p>'))
        self.assertEqual('(())', clean_up('<p>((<a class="tumblelog" href="https://tmblr.co/m6cSFDpbfSi_Lawa1EKPRUw">@0lixpox</a>)) </p>'))

    def test_html_decoding(self):
        self.assertEqual('>', clean_up('&gt;'))

    def test_spaces(self):
        self.assertEqual('some text', clean_up(' some text  '))
        self.assertEqual('some text', clean_up('some    text'))
        self.assertEqual('Some\ntext', clean_up('Some\n text'))

    def test_examples(self):
        self.assertEqual('game developers: our world is inhabited by unique creatures the likes of which you’ve never seen before!\ngame developers: and giant spiders', clean_up('<p><a href="http://balamist.tumblr.com/post/171057445484/game-developers-our-world-is-inhabited-by-unique" class="tumblr_blog">balamist</a>:</p><blockquote>\n<p><b>game developers:</b> our world is inhabited by unique creatures the likes of which you’ve never seen before!</p>\n<p><b>game developers:</b> and giant spiders</p>\n</blockquote>'))
        self.assertEqual('it’s like i always say: fuck', clean_up('<p><a href="https://imsoofuckingsad.tumblr.com/post/169627532451/its-like-i-always-say-fuck" class="tumblr_blog">imsoofuckingsad</a>:</p><blockquote><p>it’s like i always say: fuck</p></blockquote>'))
        self.assertEqual('for some reason i’m really uncomfortable with sharing my fandom ocs with people on tumblr khhh', clean_up('<p>for some reason i’m really uncomfortable with sharing my fandom <g class="gr_ gr_4 gr-alert gr_spell gr_inline_cards gr_run_anim ContextualSpelling ins-del multiReplace" id="4" data-gr-id="4">ocs</g> with people on <g class="gr_ gr_3 gr-alert gr_spell gr_inline_cards gr_run_anim ContextualSpelling ins-del multiReplace" id="3" data-gr-id="3">tumblr</g>  <g class="gr_ gr_5 gr-alert gr_spell gr_inline_cards gr_run_anim ContextualSpelling ins-del multiReplace" id="5" data-gr-id="5">khhh</g></p>'))

if __name__ == '__main__':
    unittest.main()