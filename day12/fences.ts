interface Region {
  plant: string;
  plots: Set<string>;
}

async function parse_input(filePath: string): Promise<string[]> {
  const content = await Deno.readTextFile(filePath);
  return content.trim().split("\n").map((line) => line.trimEnd());
}

function string_point_neighbors(a: string, b: string): boolean {
  const [x1, y1] = a.split(",").map(Number);
  const [x2, y2] = b.split(",").map(Number);

  return (x1 == x2 && Math.abs(y1 - y2) == 1) ||
    (y1 == y2 && Math.abs(x1 - x2) == 1);
}

function region_borders_region(region: Region, other: Region): boolean {
  if (region.plant != other.plant) return false;
  for (const a of region.plots) {
    for (const b of other.plots) {
      if (string_point_neighbors(a, b)) return true;
    }
  }
  return false;
}

function plot_borders_region(
  plant: string,
  i: number,
  j: number,
  region: Region,
): boolean {
  return region.plant == plant &&
    (region.plots.has(`${i + 1},${j}`) || region.plots.has(`${i - 1},${j}`) ||
      region.plots.has(`${i},${j + 1}`) || region.plots.has(`${i},${j - 1}`));
}

function build_simple_regions(garden: string[]): Region[] {
  const regions: Region[] = [];
  garden.forEach((row, i) => {
    [...row].forEach((plot, j) => {
      let added = false;
      for (const region of regions) {
        if (plot_borders_region(plot, i, j, region)) {
          region.plots.add(`${i},${j}`);
          added = true;
          break;
        }
      }
      if (!added) {
        regions.push({
          plant: plot,
          plots: new Set([`${i},${j}`]),
        });
      }
    });
  });
  return regions;
}

function merge_regions(regions: Region[]): Region[] {
  let changed = true;
  let current_regions = [...regions];
  while (changed) {
    changed = false;
    const new_regions: Region[] = [current_regions[0]];
    for (let i = 1; i < current_regions.length; i++) {
      let added = false;
      for (const region of new_regions) {
        if (region_borders_region(current_regions[i], region)) {
          current_regions[i].plots.forEach((plot) => region.plots.add(plot));
          added = true;
          changed = true;
          break;
        }
      }
      if (!added) {
        new_regions.push(current_regions[i]);
      }
    }
    current_regions = new_regions;
  }

  return current_regions;
}

function identify_regions(garden: string[]): Region[] {
  let regions = build_simple_regions(garden);
  regions = merge_regions(regions);
  return regions;
}

function get_perimeter(plots: Set<string>): number {
  let perimeter = 0;
  for (const plot of plots) {
    const [i, j] = plot.split(",").map(Number);
    const neighbors = [
      `${i + 1},${j}`,
      `${i - 1},${j}`,
      `${i},${j + 1}`,
      `${i},${j - 1}`,
    ];
    perimeter += neighbors.filter((neighbor) => !plots.has(neighbor)).length;
  }
  return perimeter;
}

function get_number_of_sides(plots: Set<string>): number {
  let sides = 0;
  const diffs = [1, -1];
  for (const plot of plots) {
    const [i, j] = plot.split(",").map(Number);
    sides += diffs
      .flatMap((dx) => diffs.map((dy) => [dx, dy]))
      .filter(([dx, dy]) =>
        plots.has(`${i + dx},${j}`) &&
        plots.has(`${i},${j + dy}`) &&
        !plots.has(`${i + dx},${j + dy}`)
      ).length;
    sides += diffs
      .flatMap((dx) => diffs.map((dy) => [dx, dy]))
      .filter(([dx, dy]) =>
        !plots.has(`${i + dx},${j}`) &&
        !plots.has(`${i},${j + dy}`)
      ).length;
  }
  return sides;
}

function region_fence_cost(region: Region, bulk: boolean): number {
  const area = region.plots.size;
  if (bulk) {
    const side_count = get_number_of_sides(region.plots);
    return area * side_count;
  }
  const perimeter = get_perimeter(region.plots);
  return area * perimeter;
}

function tabulate_fence_cost(regions: Region[]): number {
  const regular_cost = (region: Region) => region_fence_cost(region, false);
  return regions.map<number>(regular_cost).reduce((a, b) => a + b, 0);
}

function tabulate_bulk_fence_cost(regions: Region[]): number {
  const bulk_cost = (region: Region) => region_fence_cost(region, true);
  return regions.map<number>(bulk_cost).reduce((a, b) => a + b, 0);
}

if (import.meta.main) {
  const filePath = Deno.args[0];
  if (!filePath) {
    console.error("Please provide a file path as an argument");
    Deno.exit(1);
  }

  try {
    const contents = await parse_input(filePath);
    const regions = identify_regions(contents);
    console.log(
      `The total cost of fencing will be ${tabulate_fence_cost(regions)}`,
    );
    console.log(
      `The cost of fencing after a bulk discount will be ${
        tabulate_bulk_fence_cost(regions)
      }`,
    );
  } catch (error) {
    console.error("Error reading file:", (error as Error).message);
    Deno.exit(1);
  }
}
