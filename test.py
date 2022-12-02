from main import app
import unittest
import json

class FlaskTestCase(unittest.TestCase):
    #Ensure all pages load adn behave correctly
    #index page 
    def test_index (self):
        tester = app.test_client(self)
        response = tester.get('/index', content_type='html/text')
        self.assertEqual(response.status_code,200)
        print("Index Page Loaded Correctly")

    #home page
    def test_home (self):
        tester = app.test_client(self)
        response = tester.get('/home', content_type='html/text')
        self.assertEqual(response.status_code,200)
        print("Home Page Loaded Correctly")

    #about page
    def test_about (self):
        tester = app.test_client(self)
        response = tester.get('/about', content_type='html/text')
        self.assertEqual(response.status_code,200)
        print("About Page Loaded Correctly")

    #games page
    def test_games (self):
        tester = app.test_client(self)
        response = tester.get('/games', content_type='html/text')
        self.assertEqual(response.status_code,200)
        print("Games Page Loaded Correctly")

    #editgames page
    def test_editgames (self):
        tester = app.test_client(self)
        response = tester.get('/editgames', content_type='html/text')
        self.assertEqual(response.status_code,200)
        print("Edit Games Page Loaded Correctly")

    # Test to see if a single game details page loads correctly
    def test_single_games (self):
        tester = app.test_client(self)
        response = tester.get('/grand-theft-auto-v', content_type='html/text')
        self.assertEqual(response.status_code,200)
        print("GTAV Game Page Loaded Correctly")



    # # account page
    # def test_account (self):
    #     tester = app.test_client(self)
    #     response = tester.get('/account', content_type='html/text')
    #     self.assertEqual(response.status_code,200)
    #     print("Account Page Loaded Correctly")

    def test_add_game (self):
        tester = app.test_client(self)
        response = tester.post(
            "/games", 
            data=dict(
                gameSlug="unit-test-game",
                gameName="Unit Test Game",
                gameReleaseDate="2000-01-01",
                gameRating=1,
                gameImage="https://images7.alphacoders.com/821/thumb-1920-821837.jpg",
                gamePrice="44.99",
                gameDescription="Test Description"
            ),
            follow_redirects=True
        )
        self.assertEqual(response.status_code,200)
        print("Test Game has been added")

    #Game Deleted Correctly
    def test_delete_game (self):
        tester = app.test_client(self)
        response = tester.delete("/deleteGame/<slug>",
            data=dict(
                slug="unit-test-game",
            ),
            follow_redirects=True)
        self.assertEqual(response.status_code,200)
        print("Game deleted successfully!")

    # def test_add_invalid_game(self):
    #     tester = app.test_client(self)
    #     response = tester.post(
    #         "/games", 
    #         data=dict(
    #             gameSlug="test-game-invalid-slug",
    #             gameReleaseDate="2000-01-01",
    #             gameRating=1,
    #             gameImage="https://images7.alphacoders.com/821/thumb-1920-821837.jpg",
    #             gamePrice="44.99",
    #             gameDescription="Test Description"
    #         ),
    #         follow_redirects=True
    #     )
    #     self.assertIsNot(response.status_code,200)
    #     print("Invalid game successfully rejected")

if __name__ == "__main__":
    unittest.main()