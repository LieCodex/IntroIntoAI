using System.Collections.Generic;
using UnityEngine;

public class GameManager : MonoBehaviour
{
    private List<Tiles> OPEN = new List<Tiles>();
    private List<Tiles> CLOSED = new List<Tiles>();

    public Tiles[,] grid; // 16x9 grid
    public int width = 16;
    public int height = 9;

    private Tiles startTile;
    private Tiles goalTile;

    private bool pathFound = false;

    void Start()
    {
        // Populate the grid by finding all Tiles in the scene
        grid = new Tiles[width + 1, height + 1]; // +1 if indexing from 1

        Tiles[] allTiles = FindObjectsByType<Tiles>(FindObjectsSortMode.None);
        foreach (Tiles t in allTiles)
        {
            int gridX = Mathf.RoundToInt(t.x);
            int gridY = Mathf.RoundToInt(t.y);

            if (gridX >= 1 && gridX <= width && gridY >= 1 && gridY <= height)
            {
                grid[gridX, gridY] = t;
            }
        }

        // Assign start and goal tiles
        startTile = grid[1, 1];
        goalTile = grid[16, 9];

        startTile.gCost = 0;
        startTile.hCost = CalculateH(startTile, goalTile);
        startTile.fCost = startTile.gCost + startTile.hCost;

        OPEN.Add(startTile);

        // Start the A* search coroutine
        StartCoroutine(AStarRoutine());
    }

    private System.Collections.IEnumerator AStarRoutine()
    {
        while (OPEN.Count > 0 && !pathFound)
        {
            // Get the tile with lowest fCost
            Tiles current = GetLowestFCostTile(OPEN);

            OPEN.Remove(current);
            CLOSED.Add(current);

            // Change color for visualization
            current.GetComponent<SpriteRenderer>().color = Color.red; // explored

            // Check if we reached the goal
            if (current == goalTile)
            {
                pathFound = true;
                yield return StartCoroutine(TracePath(current));
                yield break;
            }

            // Process neighbors
            foreach (Tiles neighbor in current.GetNeighbors())
            {
                if (neighbor == null || !neighbor.walkable || CLOSED.Contains(neighbor))
                    continue;

                float newG = current.gCost + GetDistance(current, neighbor);

                if (!OPEN.Contains(neighbor) || newG < neighbor.gCost)
                {
                    neighbor.gCost = newG;
                    neighbor.hCost = CalculateH(neighbor, goalTile);
                    neighbor.fCost = neighbor.gCost + neighbor.hCost;
                    neighbor.parentNode = current;

                    if (!OPEN.Contains(neighbor))
                    {
                        OPEN.Add(neighbor);
                        neighbor.GetComponent<SpriteRenderer>().color = Color.green; // to be explored
                    }
                }
            }

            // Wait a short time to visualize step by step
            yield return new WaitForSeconds(0.05f);
        }
    }

    private Tiles GetLowestFCostTile(List<Tiles> list)
    {
        Tiles lowest = list[0];
        foreach (Tiles t in list)
        {
            if (t.fCost < lowest.fCost || (t.fCost == lowest.fCost && t.hCost < lowest.hCost))
            {
                lowest = t;
            }
        }
        return lowest;
    }

    private float CalculateH(Tiles a, Tiles b)
    {
        // Manhattan distance
        float dx = Mathf.Abs(a.x - b.x);
        float dy = Mathf.Abs(a.y - b.y);
        return (dx + dy) * 10f;
    }

    private float GetDistance(Tiles a, Tiles b)
    {
        // 10 for straight, 14 for diagonal
        float dx = Mathf.Abs(a.x - b.x);
        float dy = Mathf.Abs(a.y - b.y);

        if (dx > 0 && dy > 0)
            return 14f; // diagonal
        return 10f; // straight
    }

    private System.Collections.IEnumerator TracePath(Tiles end)
    {
        Tiles current = end;
        while (current != null)
        {
            current.GetComponent<SpriteRenderer>().color = Color.yellow; // final path
            current = current.parentNode;
            yield return new WaitForSeconds(0.05f);
        }
    }
}