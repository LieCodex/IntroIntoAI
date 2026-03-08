using NUnit.Framework;
using System.Collections.Generic;
using Unity.VisualScripting;
using UnityEngine;
using UnityEngine.EventSystems;

public class Tiles : MonoBehaviour
{

    public bool walkable;
    public float gCost = 0f;
    public float hCost = 0f;
    public float fCost = 0f;
    public Tiles parentNode;
    public float x;
    public float y;

    [SerializeField]private List<Tiles> neighbors = new List<Tiles>();  

    public LayerMask mask;

    private float multiple = 10f;


    Vector2[] directions =
    {
        Vector2.up,
        Vector2.down,
        Vector2.left,
        Vector2.right,
        new Vector2(-1, 1).normalized,
        new Vector2(1, 1).normalized,
        new Vector2(-1, -1).normalized,
        new Vector2(1, -1).normalized
    };
    // Start is called once before the first execution of Update after the MonoBehaviour is created
    private float offset = 1f;

    private void Awake()
    {
        x = transform.position.x;
        y = transform.position.y;

        foreach (Vector2 dir in directions)
        {
            Vector2 start = (Vector2)transform.position + dir * offset;

            RaycastHit2D hit = Physics2D.Raycast(start, dir, 1f, mask);

            if (hit.collider != null)
            {
                Tiles tile = hit.collider.GetComponent<Tiles>();

                if (tile != null)
                {
                    neighbors.Add(tile);
                }
            }
        }

    }
    void Start()
    {


    }
    public List<Tiles> GetNeighbors()
    {
        return neighbors;
    }

    // Update is called once per frame
    void Update()
    {
        
    }
}
