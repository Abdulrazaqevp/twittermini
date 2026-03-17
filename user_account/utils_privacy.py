def can_view_user_post(viewer, owner):
    """
determine whether viewer can see onwers's post
"""

# owner can always view
    if viewer == owner:
        return True


# public account
    if not owner.is_private:
        return True

# private acc must follow
    return owner.followers.filter(follower=viewer).exists()