interface Robot {
  x: number;
  y: number;
  dx: number;
  dy: number;
}

async function parse_input(filePath: string): Promise<Robot[]> {
  const content = await Deno.readTextFile(filePath);
  const robots: Robot[] = [];
  for (const line of content.trim().split("\n")) {
    const [pos, vel] = line.split(" ");
    const [x, y] = pos.substring(2).split(",").map(Number);
    const [dx, dy] = vel.substring(2).split(",").map(Number);
    robots.push({
      x,
      y,
      dx,
      dy,
    });
  }
  return robots;
}

function new_location(
  robot: Robot,
  seconds: number,
  height: number,
  width: number,
): number[] {
  return [
    (robot.x + robot.dx * seconds + width * seconds) % width,
    (robot.y + robot.dy * seconds + height * seconds) % height,
  ];
}

function quadrant_product(
  robots: Robot[],
  seconds: number,
  height: number,
  width: number,
): number {
  const quadrant_counts = [0, 0, 0, 0];
  for (const robot of robots) {
    const loc = new_location(robot, seconds, height, width);
    if (loc[0] > (width - 1) / 2) {
      if (loc[1] < (height - 1) / 2) {
        quadrant_counts[0]++;
      } else if (loc[1] > (height - 1) / 2) {
        quadrant_counts[3]++;
      }
    } else if (loc[0] < (width - 1) / 2) {
      if (loc[1] < (height - 1) / 2) {
        quadrant_counts[1]++;
      } else if (loc[1] > (height - 1) / 2) {
        quadrant_counts[2]++;
      }
    }
  }
  return quadrant_counts.reduce((a, b) => a * b, 1);
}

if (import.meta.main) {
  const filePath = Deno.args[0];
  if (!filePath) {
    console.error("Please provide a file path as an argument");
    Deno.exit(1);
  }

  try {
    const height = 103;
    const width = 101;
    const time = 100;
    const robots = await parse_input(filePath);
    console.log(
      `The safety factor after 100 seconds is ${
        quadrant_product(robots, time, height, width)
      }.`,
    );
  } catch (error) {
    console.error("Error reading file:", (error as Error).message);
    Deno.exit(1);
  }
}
