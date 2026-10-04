// api/_lib/social.js — shared helpers for the social API (follows, posts, reactions).
// Files under api/_lib/ are excluded from routing (underscore prefix).
const u = require('./util');

const REACTION_KINDS = ['like', 'love', 'insightful', 'celebrate'];
const VISIBILITIES = ['public', 'followers'];

async function isFollowing(sb, followerId, followedId) {
  if (!followerId || !followedId || followerId === followedId) return false;
  const { data } = await sb.from('follows')
    .select('follower_id').eq('follower_id', followerId).eq('followed_id', followedId)
    .maybeSingle();
  return !!data;
}

// Can viewerId see this post? Public = everyone except blocked either way.
// followers-only = author, or someone the author is followed by... i.e. viewer
// follows the author. Blocked either way always hides.
async function canSeePost(sb, post, viewerId) {
  if (!post) return false;
  if (viewerId && viewerId === post.user_id) return true;
  if (viewerId && await u.blockEitherWay(viewerId, post.user_id)) return false;
  if (post.visibility === 'followers') {
    if (!viewerId) return false;
    return isFollowing(sb, viewerId, post.user_id);
  }
  return true; // public
}

function authorShape(row) {
  return {
    userId: row.id,
    displayName: row.display_name,
    avatar: row.avatar,
  };
}

// Serialize one post row for API output. Loads author, shared-post snippet,
// and the viewer's own reaction (when authed).
async function serializePost(sb, post, viewerId) {
  const { data: author } = await sb.from('users')
    .select('id, display_name, avatar').eq('id', post.user_id).maybeSingle();

  let shared = null;
  if (post.shared_post_id) {
    const { data: sp } = await sb.from('posts').select('*').eq('id', post.shared_post_id).maybeSingle();
    if (sp) {
      const { data: sa } = await sb.from('users')
        .select('id, display_name, avatar').eq('id', sp.user_id).maybeSingle();
      shared = {
        id: sp.id,
        body: sp.body,
        imageUrl: sp.image_url || '',
        createdAt: sp.created_at,
        author: sa ? authorShape(sa) : null,
      };
    }
  }

  let myReaction = null;
  if (viewerId) {
    const { data: r } = await sb.from('post_reactions')
      .select('kind').eq('post_id', post.id).eq('user_id', viewerId).maybeSingle();
    if (r) myReaction = r.kind;
  }

  return {
    id: post.id,
    body: post.body,
    imageUrl: post.image_url || '',
    visibility: post.visibility,
    createdAt: post.created_at,
    likeCount: post.like_count || 0,
    commentCount: post.comment_count || 0,
    shareCount: post.share_count || 0,
    author: author ? authorShape(author) : null,
    myReaction,
    sharedPost: shared,
  };
}

async function recount(sb, table, postId, column) {
  const { count } = await sb.from(table).select('id', { count: 'exact', head: true }).eq('post_id', postId);
  await sb.from('posts').update({ [column]: count || 0 }).eq('id', postId);
  return count || 0;
}

module.exports = { REACTION_KINDS, VISIBILITIES, isFollowing, canSeePost, authorShape, serializePost, recount };
