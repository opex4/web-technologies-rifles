export interface Rifle {
    id: number;
    title: string;
    description: string;
    created_at: string;
    constructors: number[];
    country_of_origin: number;
    ammo_type: number;
    used_in_conflicts: number[];
    types_of_mounts: number[];
    picture: string | null;
}