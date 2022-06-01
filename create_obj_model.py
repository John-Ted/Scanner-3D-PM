import open3d as o3d
import numpy as np

import math

if __name__ == "__main__":
    #dataset = o3d.data.EaglePointCloud()
    pcd = o3d.io.read_point_cloud("active_rosin_2.ply")
    #o3d.io.write_point_cloud("eagle.ply", pcd, write_ascii=True)
    
    pcd.estimate_normals(
    search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.1, max_nn=30))

    distances = pcd.compute_nearest_neighbor_distance()
    avg_dist = np.mean(distances)
    radius = 3 * avg_dist

    mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(pcd, depth=12, scale=1.1, linear_fit=False)[0]

    bbox = pcd.get_axis_aligned_bounding_box()
    p_mesh_crop = mesh.crop(bbox)

    o3d.visualization.draw(p_mesh_crop)
    #o3d.io.write_triangle_mesh("multimetru_gucci.obj", p_mesh_crop)