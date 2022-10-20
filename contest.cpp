/*input
15
*/
#include<bits/stdc++.h>
//#include <ext/pb_ds/assoc_container.hpp>
//#include <ext/pb_ds/tree_policy.hpp>
//using namespace __gnu_pbds;
using namespace std;
#define ll          long long
#define pb          push_back
#define pii         pair<long,long>
#define vi          vector<long long>
#define vii         vector<pii>
#define mi          map<ll,ll>
#define mii         map<pii,ll>
#define all(a)      (a).begin(),(a).end()
#define x           first
#define y           second
#define sz(x)       (int)x.size()
#define endl        '\n'
#define hell        1000000007
#define rep(i,a,b)  for(ll i=a;i<b;i++)
#define repi(i,a,b) for(ll i=a;i>=b;i--)
#define lbnd        lower_bound
#define ubnd        upper_bound
#define bs          binary_search
#define mp          make_pair
#define fIO ios_base::sync_with_stdio(false); cin.tie(NULL); cout.tie(NULL);
#define tr(it, a) for(auto it = a.begin(); it != a.end(); it++)
#define clr(x) memset(x, 0, sizeof(x))
#define deb(x) cout << #x << "=" << x << endl
#define deb2(x, y) cout << #x << "=" << x << "," << #y << "=" << y << endl
//#define ordered_set tree<int,null_type,less<int>,rb_tree_tag, tree_order_statistics_node_update>;

ll sub(ll a, ll b){return (a-b+hell)%hell;}
ll add(ll a, ll b){return (a+b)%hell;}
ll mul(ll a, ll b){return (a*b)%hell;}
vector<ll>adj[100005];
bool vis[100005];
ll siz,edges;
void dfs(ll i)
{
	vis[i]=1;
	//siz++;
	for(ll j=0;j<adj[i].size();j++)
	{		
		edges++;
		if(!vis[adj[i][j]])
			dfs(adj[i][j]);
	}
}
const ll mod = 1000000007;
ll mpow(ll base, ll exp) {
  base %= mod;
  ll result = 1;
  while (exp > 0) {
    if (exp & 1) result = ((ll)result * base) % mod;
    base = ((ll)base * base) % mod;
    exp >>= 1;
  }
  return result;
}

int main()
{
fIO;
ll n,sum=0,t=1,m,ans;

//cin >> t;
while(t--){
	cin>>n;
	














}
	
}
