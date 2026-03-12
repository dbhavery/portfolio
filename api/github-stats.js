// Vercel Serverless Function — GitHub Stats Proxy
// Fetches aggregated stats from GitHub API, caches at edge.
// Set GITHUB_TOKEN in Vercel Environment Variables for accurate private-repo counts.
export default async function handler(req, res) {
  if (req.method !== 'GET') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const token = process.env.GITHUB_TOKEN;
  const headers = { 'Accept': 'application/vnd.github+json' };
  if (token) headers['Authorization'] = `Bearer ${token}`;

  // Fallback minimums — only upgrade, never downgrade
  const FLOOR = { totalRepos: 37, totalCommits: 1372, totalLOCKilos: 888 };

  async function ghFetch(url) {
    const resp = await fetch(url, { headers });
    if (!resp.ok) return null;
    return resp.json();
  }

  try {
    // 1. User profile (repo count)
    // 2. Repo list (metadata)
    // 3. Commit search (total count)
    // Use authenticated endpoints when token available (includes private repos)
    const userUrl = token
      ? 'https://api.github.com/user'
      : 'https://api.github.com/users/dbhavery';
    const reposUrl = token
      ? 'https://api.github.com/user/repos?per_page=100&sort=updated&type=all'
      : 'https://api.github.com/users/dbhavery/repos?per_page=100&sort=updated';

    const [user, repos, commitSearch] = await Promise.all([
      ghFetch(userUrl),
      ghFetch(reposUrl),
      ghFetch('https://api.github.com/search/commits?q=author:dbhavery')
    ]);

    let totalRepos = FLOOR.totalRepos;
    if (user) {
      const count = token
        ? (user.public_repos || 0) + (user.owned_private_repos || 0)
        : user.public_repos || 0;
      totalRepos = Math.max(count, FLOOR.totalRepos);
    }

    let totalCommits = FLOOR.totalCommits;
    if (commitSearch && commitSearch.total_count != null) {
      totalCommits = Math.max(commitSearch.total_count, FLOOR.totalCommits);
    }

    // Build repo details map
    const repoDetails = {};
    if (repos && Array.isArray(repos)) {
      repos.forEach(r => {
        repoDetails[r.name] = {
          stars: r.stargazers_count || 0,
          language: r.language || null,
          updatedAt: r.updated_at
        };
      });
    }

    // 4. Language byte counts for LOC estimation (only with token to avoid rate limits)
    let totalLOCKilos = FLOOR.totalLOCKilos;
    if (token && repos && Array.isArray(repos)) {
      const langPromises = repos.map(r =>
        ghFetch(`https://api.github.com/repos/dbhavery/${r.name}/languages`)
      );
      const langResults = await Promise.all(langPromises);
      let totalBytes = 0;
      langResults.forEach(langs => {
        if (langs) {
          Object.values(langs).forEach(bytes => { totalBytes += bytes; });
        }
      });
      // Estimate: ~40 bytes per line of code on average
      const estimatedKilos = Math.round(totalBytes / 40 / 1000);
      totalLOCKilos = Math.max(estimatedKilos, FLOOR.totalLOCKilos);
    }

    res.setHeader('Cache-Control', 'public, s-maxage=3600, stale-while-revalidate=7200');
    return res.status(200).json({
      totalRepos,
      totalCommits,
      totalLOCKilos,
      repoDetails,
      fetchedAt: new Date().toISOString()
    });
  } catch (e) {
    // On any failure, return floors so client always gets usable data
    res.setHeader('Cache-Control', 'public, s-maxage=300, stale-while-revalidate=600');
    return res.status(200).json({
      totalRepos: FLOOR.totalRepos,
      totalCommits: FLOOR.totalCommits,
      totalLOCKilos: FLOOR.totalLOCKilos,
      repoDetails: {},
      fetchedAt: new Date().toISOString(),
      fallback: true
    });
  }
}
