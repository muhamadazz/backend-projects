from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import AccessToken
from .models import Shop

User = get_user_model()

class ShopViewSetTests(APITestCase):

    def setUp(self):
        """Setup user and admin for testing."""
        self.user = User.objects.create_user(
            email='testuser@example.com',
            username='testuser',
            password='testpassword'
        )
        self.admin_user = User.objects.create_superuser(
            email='admin@example.com',
            username='admin',
            password='adminpassword'
        )
        self.user_token = AccessToken.for_user(self.user)  # Generate token for normal user
        self.admin_token = AccessToken.for_user(self.admin_user)  # Generate token for admin
        self.url = reverse('shop-list')  # Get the URL for listing shops

    def test_create_shop(self):
        """Test creating a shop."""
        response = self.client.post(
            self.url, 
            {
                'shop_name': 'New Test Shop',
                'description': 'A new test shop.',
            },
            HTTP_AUTHORIZATION=f'Bearer {self.user_token}'  # Use the user's token
        )
        print("Create Shop Response:", response.content)  # Debugging line
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, 
                         msg=f"Expected 201 Created but got {response.status_code}. Response: {response.data}")

    def test_list_user_shops(self):
        """Test listing the shops of the authenticated user."""
        self.client.post(
            self.url,
            {
                'shop_name': 'User Shop',
                'description': 'Shop for user.',
            },
            HTTP_AUTHORIZATION=f'Bearer {self.user_token}'  # Use the user's token
        )
        response = self.client.get(self.url, HTTP_AUTHORIZATION=f'Bearer {self.user_token}')  # Use the user's token
        print("List User Shops Response:", response.content)  # Debugging line
        self.assertEqual(response.status_code, status.HTTP_200_OK, 
                         msg=f"Expected 200 OK but got {response.status_code}. Response: {response.data}")
        self.assertEqual(len(response.data), 1, "User should see their own shop.")

    def test_admin_can_see_all_shops(self):
        """Test that admin can see all shops."""
        self.client.logout()  # Log out normal user
        self.client.login(username='admin', password='adminpassword')  # Log in as admin
        self.client.post(
            self.url,
            {
                'shop_name': 'Admin Shop',
                'description': 'Shop for admin.',
            },
            HTTP_AUTHORIZATION=f'Bearer {self.admin_token}'  # Use the admin's token
        )
        response = self.client.get(self.url, HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')  # Use the admin's token
        print("Admin List Shops Response:", response.content)  # Debugging line
        self.assertEqual(response.status_code, status.HTTP_200_OK, 
                         msg=f"Expected 200 OK but got {response.status_code}. Response: {response.data}")
        self.assertGreater(len(response.data), 0, "Admin should see all shops.")

    def test_update_shop(self):
        """Test updating a shop."""
        shop_response = self.client.post(
            self.url,
            {
                'shop_name': 'Shop to Update',
                'description': 'Description for update.',
            },
            HTTP_AUTHORIZATION=f'Bearer {self.user_token}'  # Use the user's token
        )
        print("Update Shop Creation Response:", shop_response.content)  # Debugging line
        self.assertEqual(shop_response.status_code, status.HTTP_201_CREATED, 
                         msg=f"Expected 201 Created but got {shop_response.status_code}. Response: {shop_response.data}")

        shop_id = shop_response.data['id']  # Get the ID of the created shop
        response = self.client.put(
            f'{self.url}{shop_id}/',
            {
                'shop_name': 'Updated Shop Name',
                'description': 'Updated Description',
            },
            HTTP_AUTHORIZATION=f'Bearer {self.user_token}'  # Use the user's token
        )
        print("Update Shop Response:", response.content)  # Debugging line
        self.assertEqual(response.status_code, status.HTTP_200_OK, 
                         msg=f"Expected 200 OK but got {response.status_code}. Response: {response.data}")

    def test_delete_shop(self):
        """Test deleting a shop."""
        shop_response = self.client.post(
            self.url,
            {
                'shop_name': 'Shop to Delete',
                'description': 'Description',
            },
            HTTP_AUTHORIZATION=f'Bearer {self.user_token}'  # Use the user's token
        )
        print("Delete Shop Creation Response:", shop_response.content)  # Debugging line
        self.assertEqual(shop_response.status_code, status.HTTP_201_CREATED, 
                         msg=f"Expected 201 Created but got {shop_response.status_code}. Response: {shop_response.data}")

        shop_id = shop_response.data['id']  # Get the ID of the created shop
        response = self.client.delete(f'{self.url}{shop_id}/', 
                                       HTTP_AUTHORIZATION=f'Bearer {self.user_token}')  # Use the user's token
        print("Delete Shop Response:", response.content)  # Debugging line
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT, 
                         msg=f"Expected 204 No Content but got {response.status_code}. Response: {response.data}")

    def test_create_shop_duplicate_name(self):
        """Test creating a shop with a duplicate name."""
        self.client.post(
            self.url,
            {
                'shop_name': 'Duplicate Shop',
                'description': 'First shop with this name.',
            },
            HTTP_AUTHORIZATION=f'Bearer {self.user_token}'  # Use the user's token
        )
        response = self.client.post(
            self.url,
            {
                'shop_name': 'Duplicate Shop',  # Same name as existing shop
                'description': 'Attempt to create duplicate shop.',
            },
            HTTP_AUTHORIZATION=f'Bearer {self.user_token}'  # Use the user's token
        )
        print("Create Duplicate Shop Response:", response.content)  # Debugging line
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, 
                         msg=f"Expected 400 Bad Request but got {response.status_code}. Response: {response.data}")

    def test_update_shop_not_found(self):
        """Test updating a shop that doesn't exist."""
        response = self.client.put(reverse('shop-detail', args=[999]), {
            'shop_name': 'Non-existing Shop',
        }, HTTP_AUTHORIZATION=f'Bearer {self.user_token}')  # Use the user's token
        print("Update Non-existing Shop Response:", response.content)  # Debugging line
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND, 
                         msg=f"Expected 404 Not Found but got {response.status_code}. Response: {response.data}")

    def test_delete_shop_not_found(self):
        """Test deleting a shop that doesn't exist."""
        response = self.client.delete(reverse('shop-detail', args=[999]), 
                                       HTTP_AUTHORIZATION=f'Bearer {self.user_token}')  # Use the user's token
        print("Delete Non-existing Shop Response:", response.content)  # Debugging line
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND, 
                         msg=f"Expected 404 Not Found but got {response.status_code}. Response: {response.data}")

    def test_create_shop_without_authentication(self):
        """Test creating a shop without authentication."""
        self.client.logout()  # Log out the user
        response = self.client.post(self.url, {
            'shop_name': 'Unauthenticated Shop',
            'description': 'Should not be created.',
        })
        print("Create Shop Without Authentication Response:", response.content)  # Debugging line
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED, 
                         msg=f"Expected 401 Unauthorized but got {response.status_code}. Response: {response.data}")

    def test_create_shop_invalid_data(self):
        """Test creating a shop with invalid data (missing shop_name)."""
        response = self.client.post(self.url, {
            'description': 'Shop without a name.',
            'is_active': True,
        }, HTTP_AUTHORIZATION=f'Bearer {self.user_token}')  # Use the user's token
        print("Create Shop Invalid Data Response:", response.content)  # Debugging line
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, 
                         msg=f"Expected 400 Bad Request but got {response.status_code}. Response: {response.data}")
        self.assertIn('shop_name', response.data, "Error related to shop_name should be present.")

    def test_user_can_only_see_own_shops(self):
        """Test that user can only see their own shops."""
        # Create a shop for the user
        self.client.post(
            self.url,
            {
                'shop_name': 'User Shop',
                'description': 'Shop for user.',
            },
            HTTP_AUTHORIZATION=f'Bearer {self.user_token}'  # Use the user's token
        )
        
        # Create another shop for the admin user
        Shop.objects.create(user=self.admin_user, shop_name='Admin Shop', description='Shop for admin.')
        
        # Now check if the user can see their own shop
        response = self.client.get(self.url, HTTP_AUTHORIZATION=f'Bearer {self.user_token}')  # Use the user's token
        print("User List Own Shops Response:", response.content)  # Debugging line
        self.assertEqual(response.status_code, status.HTTP_200_OK, 
                        msg=f"Expected 200 OK but got {response.status_code}. Response: {response.data}")
        self.assertEqual(len(response.data), 1, "User should only see their own shop.")

