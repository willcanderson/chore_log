from django.test import Client, TestCase

from .models import User, Chore_Definition, Work, Play

# Create your tests here.
class ChoreLogTestCase(TestCase):

    def setUp(self):

        # Create objects
        parent1 = User.objects.create(username="Dad", user_type="PARENT")
        child1 = User.objects.create(username="Kid", user_type="CHILD", parent=parent1)
        chore1 = Chore_Definition.objects.create(name="Wash car", minute_value=40, defined_by=parent1)
        chore2 = Chore_Definition.objects.create(name="Fold laundry", minute_value=15, defined_by=parent1)
        work1 = Work.objects.create(chore=chore1, done_by=child1)
        work2 = Work.objects.create(chore=chore2, done_by=child1)
        play1 = Play.objects.create(game="Zelda", minutes_played=45, child=child1)
        play2 = Play.objects.create(game="Mario", minutes_played=-1, child=child1)

    # Test models
    def test_parent_relationship(self):
        dad = User.objects.get(username="Dad")
        kid = User.objects.get(username="Kid")
        self.assertEqual(kid.parent, dad)

    def test_valid_play(self):
        play = Play.objects.get(game="Zelda")
        self.assertTrue(play.is_valid_play())

    def test_invalid_play(self):
        play = Play.objects.get(game="Mario")
        self.assertFalse(play.is_valid_play())

    # Test pages
    def test_start_page(self):
        c = Client()
        response = c.get("/chorelogapp/")
        self.assertEqual(response.status_code, 200)

    def test_parent_index(self):
        c = Client()
        self.user = User.objects.get(username="Dad")
        c.force_login(self.user)
        response = c.get("/chorelogapp/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["child_list"]), 1)
        self.assertEqual(len(response.context["chores"]), 2)

    def test_child_index(self):
        c = Client()
        self.user = User.objects.get(username="Kid")
        c.force_login(self.user)
        response = c.get("/chorelogapp/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["log_items"]), 4)

    def test_full_log(self):
        c = Client()
        self.user = User.objects.get(username="Kid")
        c.force_login(self.user)
        response = c.get(f"/chorelogapp/log/{self.user.username}")
        self.assertEqual(response.status_code, 200)

    def test_full_log_permissions(self):
        c = Client()
        parent = User.objects.get(username="Dad")
        child = User.objects.get(username="Kid")
        self.user = User.objects.create(username="DifferentKid", user_type="CHILD", parent=parent)
        c.force_login(self.user)
        response = c.get(f"/chorelogapp/log/{child.username}")
        # Should redirect the user
        self.assertEqual(response.status_code, 302)
